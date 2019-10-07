using System;
using System.Data;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace SettlementTool
{
    public partial class FormReceiveMail : Form
    {
        private encrypt cEncrypt = null;

        public FormReceiveMail()
        {
            InitializeComponent();
        }

        private void FormReceiveMail_Load(object sender, EventArgs e)
        {
            cEncrypt = new encrypt();
            RefreshData();
        }

        /// <summary>
        /// 刷新界面所有数据，数据来源数据库
        /// </summary>
        private void RefreshData()
        {
            string sql = "select pathname, path from pathlist where pathname in ('Pop3Address', 'SSL', 'Pop3port', 'username', 'password');";
            MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
            MySqlDataAdapter data = new MySqlDataAdapter(cmd);
            DataSet ds = new DataSet();
            data.Fill(ds);
            foreach (DataRow iRow in ds.Tables[0].Rows)
            {
                switch (iRow["pathname"].ToString())
                {
                    default:
                        break;
                    case "Pop3Address":
                        txtPop3address.Text = iRow["path"].ToString();
                        break;
                    case "SSL":
                        if (iRow["path"].Equals("1"))
                            chkSSL.Checked = true;
                        else
                            chkSSL.Checked = false;
                        break;
                    case "Pop3port":
                        txtPort.Text = iRow["path"].ToString();
                        break;
                    case "username":
                        txtUsername.Text = iRow["path"].ToString();
                        break;
                    case "password":
                        string sPassword = iRow["path"].ToString();
                        if (sPassword == "")
                            txtPassword.Text = "";
                        else
                            txtPassword.Text = cEncrypt.Decrypt(sPassword, "SettleDH");
                        break;
                }
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            string sSql = "delete from pathlist where pathname in ('Pop3Address', 'SSL', 'Pop3port', 'username', 'password');";
            sSql += "insert into pathlist(pathname, path) values";
            sSql += "('Pop3Address','" + txtPop3address.Text.Trim() + "'), ";
            if (chkSSL.Checked)
                sSql += "('SSL','1'),";
            else
                sSql += "('SSL','0'),";
            sSql += "('Pop3port','" + txtPort.Text.Trim() + "'),";
            sSql += "('username','" + txtUsername.Text.Trim() + "'),";
            sSql += "('password','" + cEncrypt.Encrypt(txtPassword.Text.Trim(), "SettleDH") + "');";
            System.Diagnostics.Debug.Assert(false, sSql);

            MySqlCommand cmd = new MySqlCommand(sSql, FormMain.conn);
            try
            {
                cmd.ExecuteNonQuery();
            }
            catch (Exception ex)
            {
                MessageBox.Show("SQL执行异常：" + ex.Message);
            }

            RefreshData();
        }

        private void btnTest_Click(object sender, EventArgs e)
        {
            Pop3 testMailConnect = new Pop3();
            testMailConnect.HostName = txtPop3address.Text.Trim();
            testMailConnect.Port = int.Parse(txtPort.Text.Trim());
            try
            {
                if (!testMailConnect.Connect())
                    MessageBox.Show("连接邮件服务器失败！");
                string ErrMsg = "";
                if (testMailConnect.login(txtUsername.Text.Trim(), txtPassword.Text.Trim(), ref ErrMsg))
                    MessageBox.Show("测试连接成功！");
                else
                    MessageBox.Show("测试连接失败！" + ErrMsg);
            }
            catch (Exception ex)
            {
                MessageBox.Show("测试连接失败：" + ex.Message.ToString());
            }
            
        }
    }
}
