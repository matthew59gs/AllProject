using System.Windows.Forms;
using System;
using System.Data;
using MySql.Data.MySqlClient;
using System.Drawing;
using System.Text;
using System.Security.Cryptography;
using System.Collections.Generic;
using log4net;
using System.Threading;
using OpenPop.Pop3;
using OpenPop.Mime;
using OpenPop.Mime.Header;
using System.IO;

namespace SettlementTool
{
    /// <summary>
    /// 主窗体
    /// </summary>
    public partial class FormMain : Form
    {
        #region 全局变量
        /// <summary>
        /// 全局公用数据库连接 
        /// </summary>
        public static MySqlConnection conn = null;

        /// <summary>
        /// 工作日
        /// </summary>
        public DateTime Dealdate_;

        /// <summary>
        ///  邮箱连接参数
        /// </summary>
        private string sHost = "", username = "", password = "";
        private int iPort = 0;

        List<BrokerMailInfo> brokermaillist = null;
        List<RenameInfo> renameinfolist = null;

        /// <summary>
        /// 文件路径参数
        /// </summary>
        private const string PATHSEPERATE = @"\";
        private string BaseDir = "";
        private string DatePrex = "";
        private const string NORMALPREX = @"normal\";
        private const string ORIPREX = @"originaldata\";
        private List<string> FundcodePath;
        private List<string> BrokerNamePath;    //[No]Name这样的形式
        /// <summary>
        /// 进度条
        /// </summary>
        processbar pb = null;
        /// <summary>
        /// 日志对象
        /// </summary>
        public static ILog log;
        /// <summary>
        /// 输出文本到显示框的显示级别
        /// </summary>
        private enum InfoType { INFO, WARNING, ERROR };
        #endregion

        public FormMain()
        {
            // 界面初始化
            InitializeComponent();
        }

        /// <summary>
        /// 刷新数据库的数据给前台
        /// </summary>
        /// <remarks>这里使用MySqlDataReader而不是MySqlDataAdapter</remarks>
        private void RefreshDBData()
        {
            Dealdate_ = dateDeal.Value;
#if DEBUG
            Dealdate_ = new DateTime(2016, 6, 27, 0, 0, 0);
#endif
            DatePrex = Dealdate_.ToString("yyyy-MM-dd") + PATHSEPERATE;
            /// 基础路径获取
            string sql = @"select path from pathlist where pathname = 'Main';";
            MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
            MySqlDataReader reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                if (reader.HasRows)
                {
                    BaseDir = reader.GetString(0);
                }
            }
            reader.Close();
            if (BaseDir.LastIndexOf(PATHSEPERATE) != BaseDir.Length - 1)
                BaseDir += PATHSEPERATE;

            /// 取收件箱设置
            sql = "select pathname, path from pathlist where pathname in ('Pop3Address', 'SSL', 'Pop3port', 'username', 'password');";
            cmd.CommandText = sql;
            reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                if (reader.HasRows)
                {
                    switch (reader.GetString(0))
                    {
                        default:
                            break;
                        case "Pop3Address":
                            sHost = reader.GetString(1);
                            break;
                        case "Pop3port":
                            iPort = reader.GetInt32(1);
                            break;
                        case "username":
                            username = reader.GetString(1);
                            break;
                        case "password":
                            password = (new encrypt()).Decrypt(reader.GetString(1), "SettleDH");
                            break;
                    }
                    ;
                }
            }
            reader.Close();

            /// 从数据库取券商邮箱设置
            brokermaillist.Clear();
            BrokerNamePath.Clear();
            sql = "select no, brokername as '券商名称', mailaddress as '邮箱地址', subject as '关键字' from maillist where valid = 1;";
            cmd.CommandText = sql;
            reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                if (reader.HasRows)
                {
                    BrokerMailInfo aBrokermailinfo = new BrokerMailInfo();
                    aBrokermailinfo.no_pro = reader.GetString(0);
                    aBrokermailinfo.brokername_pro = reader.GetString(1);
                    aBrokermailinfo.mailaddress_pro = reader.GetString(2);
                    aBrokermailinfo.subject_pro = reader.GetString(3);
                    brokermaillist.Add(aBrokermailinfo);
                    BrokerNamePath.Add(BaseDir + DatePrex + ORIPREX + "[" + aBrokermailinfo.no_pro + "]" + aBrokermailinfo.brokername_pro + PATHSEPERATE);
                }
            }
            reader.Close();

            /// 从数据库取基金重命名规则
            renameinfolist.Clear();
            FundcodePath.Clear();
            sql = "select fundcode as '基金代码', fundname as '基金名称', brokercode as '券商代码', oldpattern as '原始文件格式', newpattern as '目标文件格式' from renamelist;";
            cmd.CommandText = sql;
            reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                if (reader.HasRows)
                {
                    RenameInfo aRenameInfo = new RenameInfo();
                    aRenameInfo.fundcode = reader.GetString(0);
                    aRenameInfo.fundname = reader.GetString(1);
                    aRenameInfo.brokercode = reader.GetString(2);
                    aRenameInfo.oldpattern = reader.GetString(3);
                    aRenameInfo.newpattern = reader.GetString(4);
                    renameinfolist.Add(aRenameInfo);
                    FundcodePath.Add(BaseDir + DatePrex + NORMALPREX + aRenameInfo.fundcode + PATHSEPERATE);
                }
            }
            reader.Close();
        }
        /// <summary>
        /// 按照路径生成文件夹
        /// </summary>
        private void MakeDir()
        {
            if (BrokerNamePath.Count > 0)
            {
                foreach (string path in BrokerNamePath)
                {
                    if (!Directory.Exists(path))
                        Directory.CreateDirectory(path);
                }
            }
            if (FundcodePath.Count > 0)
            {
                foreach (string path in FundcodePath)
                {
                    if (!Directory.Exists(path))
                        Directory.CreateDirectory(path);
                }
            }
        }
        /// <summary>
        /// 从邮件的From字段，获取本地的附件存放路径
        /// </summary>
        /// <param name="from">邮件的From字段</param>
        /// <returns></returns>
        private string GetPathFromMailFrom(string from)
        {
            for (int i = 0; i < brokermaillist.Count; ++i)
            {
                BrokerMailInfo aBrokerInfo = brokermaillist[i];
                if (from.IndexOf(aBrokerInfo.mailaddress_pro) >= 0)
                    return BrokerNamePath[i];
            }
            return "";
        }

        /// <summary>
        /// 检查邮件是否属于券商列表中
        /// </summary>
        /// <param name="header">待检查的邮件头</param>
        /// <returns></returns>
        private bool CheckInBrokerList(OpenPop.Mime.Header.MessageHeader header)
        {
            for (int i = 0; i < brokermaillist.Count; ++i)
            {
                if (header.From.Address.IndexOf(brokermaillist[i].mailaddress_pro) >= 0)
                {
                    if (header.Subject.IndexOf(brokermaillist[i].subject_pro) >= 0)
                        return true;
                }
            }
            return false;
        }

        private void showInfo(string Info, InfoType i = InfoType.INFO)
        {
            Color oriColor;
            string sInfo = "";
            switch (i)
            {
                default:
                    break;
                case InfoType.INFO:
                    sInfo = "[信息]" + Info + "\n";
                    txtInfo.AppendText(sInfo);
                    log.Info(Info);
                    break;
                case InfoType.WARNING:
                    sInfo = "[警告]" + Info + "\n";
                    oriColor = txtInfo.SelectionColor;
                    txtInfo.SelectionColor = Color.Blue;
                    txtInfo.AppendText(sInfo);
                    txtInfo.SelectionColor = oriColor;
                    txtInfo.Refresh();
                    log.Warn(Info);
                    break;
                case InfoType.ERROR:
                    sInfo = "[错误]" + Info + "\n";
                    oriColor = txtInfo.SelectionColor;
                    txtInfo.SelectionColor = Color.Red;
                    txtInfo.AppendText(sInfo);
                    txtInfo.SelectionColor = oriColor;
                    txtInfo.Refresh();
                    log.Error(Info);
                    break;
            }
            
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (conn != null)
            {
                if (conn.State == ConnectionState.Open)
                {
                    txtDB.Text = "数据库已经连接";
                    txtDB.ForeColor = Color.Black;
                }
                else
                {
                    txtDB.Text = "数据库尚未连接";
                    txtDB.ForeColor = Color.Red;
                }
            }
            else
            {
                txtDB.Text = "数据库尚未连接";
                txtDB.ForeColor = Color.Red;
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            conn = new MySqlConnection("server=localhost;User Id=root;password=123456;Database=settle;Charset=utf8");
            dateDeal.Value = System.DateTime.Now;
            brokermaillist = new List<BrokerMailInfo>();
            renameinfolist = new List<RenameInfo>();
            BrokerNamePath = new List<string>();
            FundcodePath = new List<string>();
            log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            if (conn != null)
                conn.Close();
        }

        private void btnConnectDB_Click(object sender, EventArgs e)
        {
            if (conn != null)
            {
                if (conn.State != ConnectionState.Open)
                {
                    try
                    {
                        conn.Open();
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show("Failed to open database:/n" + ex.Message);
                    }
                }
            }
        }

        private void 券商邮箱设置ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form FrmMail = new FormMail();
            FrmMail.Top = this.Top + this.Height / 4;
            FrmMail.Left = this.Left + this.Width / 4;
            FrmMail.ShowDialog();
        }

        private void 重命名格式设置ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form FrmRename = new FormRename();
            FrmRename.Top = this.Top + this.Height / 4;
            FrmRename.Left = this.Left + this.Width / 4;
            FrmRename.ShowDialog();
        }

        private void 邮件收取路径ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form Frmpath = new FormPath();
            Frmpath.Top = this.Top + this.Height / 4;
            Frmpath.Left = this.Left + this.Width / 4;
            Frmpath.ShowDialog();
        }

        private void 接收邮箱设置ToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form FrmRecieveMail = new FormReceiveMail();
            FrmRecieveMail.Top = this.Top + this.Height / 4;
            FrmRecieveMail.Left = this.Left + this.Width / 4;
            FrmRecieveMail.ShowDialog();
        }

        private void btnMail_Click(object sender, EventArgs e)
        {
            log.Info("刷新数据库基础数据");
            RefreshDBData();
            MakeDir();
            int iUndealCount = 0;

            /// 连接邮件服务器
            
            Pop3Client client = new Pop3Client();
            try
            {
                /// 邮件处理失败，有InvalidLoginException抛出
                log.Info("连接邮箱，地址：" + sHost + ":" + iPort.ToString());
                client.Connect(sHost, iPort, true);
                showInfo("连接服务器" + sHost + "成功");

                /// 登录失败，有InvalidUseException抛出
                log.Info("登录邮箱，用户名：" + username);
                client.Authenticate(username, password);
                showInfo("登录" + username + "成功");

                int messageCount = client.GetMessageCount();
                showInfo("收取" + messageCount.ToString() + "封邮件");
                List<OpenPop.Mime.Message> allMessages = new List<OpenPop.Mime.Message>(messageCount);
                for (int i = 1; i <= messageCount; ++i)
                {
                    #region 收取邮件
                    /// GetMessageHeaders的参数messageNumber字段范围是[1, MessageCount]
                    MessageHeader messageheader = client.GetMessageHeaders(i);
                    #endregion

                    #region 邮件检查
                    if (Dealdate_.Date.ToString("yyyy-MM-dd") != messageheader.DateSent.ToString("yyyy-MM-dd"))
                        continue;
                    if (!CheckInBrokerList(messageheader))
                        continue;
                    ++iUndealCount;
                    /// GetMessage的参数messageNumber字段范围是[1, MessageCount]
                    OpenPop.Mime.Message message = client.GetMessage(i);
                    List<MessagePart> attachments = message.FindAllAttachments();
#if DEBUG
                    showInfo("收取有效邮件\nFrom:" + messageheader.From.Address + "\nSubject:" + messageheader.Subject + "\nAttachmentCount:" + attachments.Count.ToString() + "\n", InfoType.WARNING);
#else
                    log.Info("收取有效邮件\nFrom:" + messageheader.From.Address + "\nSubject:" + messageheader.Subject + "\nAttachmentCount:" + attachments.Count.ToString() + "\n");
#endif
                    #endregion

                    #region 保存附件
                    string path = GetPathFromMailFrom(messageheader.From.Address);
                    if (path != "")
                    {
                        foreach (MessagePart attachment in attachments)
                        {
                            FileInfo fi = new FileInfo(path + attachment.FileName);
                            attachment.Save(fi);
                        }
                    }
                    #endregion
                }

                if (iUndealCount == 0)
                    showInfo("没有收到需要处理的邮件！");
                else
                    showInfo("成功处理邮件" + iUndealCount.ToString() + "封");
            }
            catch (Exception ex)
            {
                log.Error("邮件处理失败：" + ex.Message.ToString());
                MessageBox.Show("邮件处理失败：" + ex.Message.ToString());
            }

        }
    }
}
