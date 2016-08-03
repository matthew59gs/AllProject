using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.Odbc;
using System.Data.OleDb;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CATS_DBFReader
{
    public partial class FormMain : Form
    {
        public string strDBF = "";
        public bool isConnect = false;

        public object Fileinfo { get; private set; }

        public FormMain()
        {
            InitializeComponent();
            RefreshData();
        }

        public void RefreshData()
        {
            if (!isConnect)
            {
                return;
            }
            else
            {
                try
                {

                }
                catch (Exception ex)
                {
                    isConnect = false;
                    MessageBox.Show(ex.Message);
                }
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            RefreshData();
        }

        private void btnBrowse_Click(object sender, EventArgs e)
        {
            OpenFileDialog file = new OpenFileDialog();
            if (txtPath.Text.Trim() != "")
            {
                file.FileName = txtPath.Text.Trim();
            }
            if (file.ShowDialog() == DialogResult.OK)
            {
                txtPath.Text = file.FileName;
            }
        }

        private void btnLink_Click(object sender, EventArgs e)
        {
            isConnect = false;
            string DBFPath = txtPath.Text.Trim();
            if (DBFPath != "")
            {
                try
                {
                    FileInfo fi = new FileInfo(DBFPath);
                    string directory = fi.DirectoryName;
                    string filename = fi.Name;

                    // DBF连接打开
                    string connStr = @" Driver={Microsoft dBASE Driver (*.dbf)}; SourceType=DBF; " +
                    @" Data Source=" + DBFPath + "; Exclusive=No; NULL=NO; " +
                    @" Collate=Machine; BACKGROUNDFETCH=NO; DELETE=NO";
                    OdbcConnection conn = new OdbcConnection(connStr);
                    conn.Open();
                    // 以SQL方式查询
                    string sql = @"select * from " + filename;
                    OdbcDataAdapter da = new OdbcDataAdapter(sql, conn);
                    DataSet ds = new DataSet();
                    da.Fill(ds);
                    dataGridData.DataSource = ds.Tables[0];
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }
    }
}
