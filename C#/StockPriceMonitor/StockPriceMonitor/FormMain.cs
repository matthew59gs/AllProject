using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using log4net;
using MySql.Data.MySqlClient;
using WAPIWrapperCSharp;

namespace StockPriceMonitor
{
    public partial class FormMain : Form
    {
        #region 全局变量
        /// <summary>
        /// 全局公用数据库连接 
        /// </summary>
        public static MySqlConnection conn = null;

        /// <summary>
        /// 日志对象
        /// </summary>
        public static ILog log;

        /// <summary>
        /// 万得API相关
        /// </summary>
        public static WindAPI w = new WindAPI();    // API对象
        public delegate void WindCallback(ulong reqId, WindData wd);    // 回调委托
        WindCallback wc = null;     // 回调实例
        ulong WDreqId = 0;          // 订阅实时行情的订阅编号                                                 

        List<StockInfo> stockList = null;
        List<StockInfo> BaseStockList = null;
        bool bStartMonit = false;
        new Color DefaultBackColor = Color.Black;
        System.Media.SoundPlayer sp = null;
        int PlayTime = 0;
        const int PlayInterval = 600;
        #endregion

        public FormMain()
        {
            InitializeComponent();
        }

        private void FormMain_Load(object sender, EventArgs e)
        {
            log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType);

            /// 连接数据库
            conn = new MySqlConnection("server=localhost;User Id=root;password=123456;Database=stock_monitor;Charset=utf8");
            if (conn.State != ConnectionState.Open)
            {
                try
                {
                    conn.Open();
                    log.Info("database stock_monitor conneted.");
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Failed to open database:/n" + ex.Message + "\nPlease reopen the program");
                    log.Error("database stock_monitor fail to connet. " + ex.Message);
                }
            }

            /// 登录WIND
            wc = new WindCallback(RefreshHQ);
            int LogonResult = (int)w.start("", "", 5000);
            if (LogonResult != 0)
            {
                MessageBox.Show("登陆失败！" + Environment.NewLine + "请检查Wind终端是否打开。错误码" + LogonResult);
                return;
            }

            /// 提取音乐
            sp = new System.Media.SoundPlayer(Resource1.warn);

            stockList = new List<StockInfo>();
            BaseStockList = new List<StockInfo>();
            DefaultBackColor = dataGridView1.DefaultCellStyle.BackColor;
        }

        private void btnModify_Click(object sender, EventArgs e)
        {
            Form FrmModify = new FormModify();
            FrmModify.Top = this.Top + this.Height / 4;
            FrmModify.Left = this.Left + this.Width / 4;
            FrmModify.ShowDialog();
        }

        private void btnStart_Click(object sender, EventArgs e)
        {
            if (!bStartMonit)
            {
                /// 从数据库读取数据
                stockList.Clear();
                string sql = @"select stock_code, monitor_price, direction from stock_monitor;";
                MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
                MySqlDataReader reader = cmd.ExecuteReader();
                while (reader.Read())
                {
                    if (reader.HasRows)
                    {
                        StockInfo aInfo = new StockInfo();
                        aInfo.stock_code = reader.GetString(0).ToUpper();
                        aInfo.monit_price = reader.GetString(1); 
                        aInfo.direction = reader.GetInt32(2);
                        stockList.Add(aInfo);
                    }
                }
                reader.Close();

                /// 加载基础信息
                BaseStockList.Clear();
                WindData wd = w.wset("sectorconstituent", "date=2016-07-05;sectorid=a001010100000000");
                int clength = wd.codeList.Length, flength = wd.fieldList.Length, tlength = wd.timeList.Length;
                /// odata格式：date(日期), wind_code(wind代码), sec_name(证券名称)
                object[,] odata = (object[,])wd.getDataByFunc("wset", false);
                for (int i = 0; i < clength; ++i)
                {
                    StockInfo aInfo = new StockInfo();
                    aInfo.stock_code = string.Format("{0}", odata[i, 1]).ToUpper();
                    aInfo.stock_name = string.Format("{0}", odata[i, 2]);
                    BaseStockList.Add(aInfo);
                }
                for (int i = 0; i < stockList.Count; ++i)
                    for (int j = 0; j < BaseStockList.Count; ++j)
                        if (stockList[i].stock_code == BaseStockList[j].stock_code)
                        {
                            var aInfo = stockList[i];
                            aInfo.stock_name = BaseStockList[j].stock_name;
                            stockList[i] = aInfo;
                        }


                /// 订阅实时行情
                int errorId = 0;
                string CodeList = "";
                for (int i = 0; i < stockList.Count; ++i)
                    CodeList += stockList[i].stock_code + ",";
                CodeList = CodeList.Substring(0, CodeList.Length - 1);
                WDreqId = w.wsq(ref errorId, CodeList, "rt_last,rt_pct_chg", "", RefreshHQ);
                if (errorId != 0)
                    MessageBox.Show("订阅万得行情信息失败：" + w.getErrorMsg(errorId));
                else
                {
                    bStartMonit = true;
                    btnStart.Text = "停止监控";
                }
            }
            else
            {
                w.cancelRequest(WDreqId);
                btnStart.Text = "开始监控";
                bStartMonit = false;
            }
        }

        private void RefreshHQ(ulong reqId, WindData wd)
        {
            int clength = wd.codeList.Length, flength = wd.fieldList.Length, tlength = wd.timeList.Length;
            /// odata格式：rt_last(最新价),rt_pct_chg(涨跌幅)
            object[,] odata = (object[,])wd.getDataByFunc("wsq", false);
            for (int i = 0; i < stockList.Count; ++i)
            {
                var aInfo = stockList[i];
                aInfo.last_price = string.Format("{0}", odata[i, 0]);
                aInfo.chg = string.Format("{0}", odata[i, 1]);
                stockList[i] = aInfo;
            }
        }

        private void RefreshGrid()
        {
            if (stockList.Count == 0)
                return;

            dataGridView1.ColumnCount = StockInfo.VisibleField;
            dataGridView1.RowCount = stockList.Count();
            dataGridView1.RowHeadersDefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
            dataGridView1.RowHeadersWidth = 10;
            // 列表头
            dataGridView1.Columns[0].HeaderText = "代码";
            dataGridView1.Columns[1].HeaderText = "名称";
            dataGridView1.Columns[2].HeaderText = "最新价";
            dataGridView1.Columns[3].HeaderText = "涨跌幅";
            dataGridView1.Columns[4].HeaderText = "监控价格";

            double last_price =0, monit_price = 0, chg = 0;
            for (int i = 0; i < stockList.Count; ++i)
            {
                dataGridView1.Rows[i].Cells[0].Value = stockList[i].stock_code;
                dataGridView1.Rows[i].Cells[1].Value = stockList[i].stock_name;
                dataGridView1.Rows[i].Cells[2].Value = string.Format("{0:N3}", stockList[i].last_price);
                if (stockList[i].chg != null)
                    chg = float.Parse(stockList[i].chg);
                if (chg > 0)
                    dataGridView1.Rows[i].Cells[3].Style.ForeColor = Color.Red;
                else if (chg < 0)
                    dataGridView1.Rows[i].Cells[3].Style.ForeColor = Color.Green;
                else
                    dataGridView1.Rows[i].Cells[3].Style.ForeColor = Color.Gray;
                dataGridView1.Rows[i].Cells[3].Value = string.Format("{0:P}", chg);
                dataGridView1.Rows[i].Cells[4].Value = string.Format("{0:N3}", stockList[i].monit_price);

                // 触警变化
                if (bStartMonit)
                {
                    if (stockList[i].last_price != null)
                        last_price = float.Parse(stockList[i].last_price);
                    if (stockList[i].monit_price != null)
                        monit_price = float.Parse(stockList[i].monit_price);
                    if (last_price != 0 && monit_price != 0)
                    {
                        switch (stockList[i].direction)
                        {
                            default:
                                break;
                            case 1:     //小于
                                if (last_price < monit_price)
                                {
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = Color.Orange;
                                    playMusic();
                                }
                                else
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = DefaultBackColor;
                                break;
                            case 2:     // 小于等于
                                if (last_price <= monit_price)
                                {
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = Color.Orange;
                                    playMusic();
                                }
                                else
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = DefaultBackColor;
                                break;
                            case 3:     // 大于
                                if (last_price > monit_price)
                                {
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = Color.Orange;
                                    playMusic();
                                }
                                else
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = DefaultBackColor;
                                break;
                            case 4:     // 大于等于
                                if (last_price >= monit_price)
                                {
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = Color.Orange;
                                    playMusic();
                                }
                                else
                                    dataGridView1.Rows[i].DefaultCellStyle.BackColor = DefaultBackColor;
                                break;
                        }
                    }
                }
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            RefreshGrid();
        }

        private void playMusic()
        {
            if (PlayTime == 0)
                sp.Play();
            PlayTime++;
            if (PlayTime == PlayInterval)
                PlayTime = 0;
        }
    }


    public struct StockInfo
    {
        public const int VisibleField = 5;
        public string stock_code;   // 代码
        public string stock_name;   // 名称
        public string last_price;   // 最新价
        public string chg;          // 涨跌幅
        public string monit_price;  // 监控价格
        public int direction;       // 比较方向
    }
}
