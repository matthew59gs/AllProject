using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace StockPriceMonitor
{
    public partial class FormModify : Form
    {
        public FormModify()
        {
            InitializeComponent();
        }

        private void FormModify_Load(object sender, EventArgs e)
        {
            dataGridView1.ReadOnly = true;
            dataGridView1.AllowUserToAddRows = false;
            dataGridView1.AllowUserToDeleteRows = false;

            RefreshDB();
        }

        private void RefreshDB()
        {
            if (FormMain.conn.State != ConnectionState.Open)
                MessageBox.Show("数据库未连接，关闭后重新打开此程序！");
            else
            {
                string sql = @"select stock_code as '股票代码', monitor_price as '监控价格', case direction when 1 then '小于' when 2 then '小于等于' when 3 then '大于' when 4 then '大于等于' else '' end as '方向' from stock_monitor;";
                MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
                MySqlDataAdapter data = new MySqlDataAdapter(cmd);
                DataSet ds = new DataSet();
                data.Fill(ds);
                dataGridView1.DataSource = ds.Tables[0];
            }
        }

        private void btnModify_Click(object sender, EventArgs e)
        {
            dataGridView1.AllowUserToAddRows = true;
            dataGridView1.AllowUserToDeleteRows = true;
            dataGridView1.ReadOnly = false;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            dataGridView1.AllowUserToAddRows = false;
            dataGridView1.AllowUserToDeleteRows = false;
            dataGridView1.ReadOnly = true;

            string sSql = "DELETE from stock_monitor;";
            foreach (DataGridViewRow iRow in dataGridView1.Rows)
            {
                sSql += "insert into stock_monitor(stock_code, monitor_price, direction) values(";
                sSql += "'" + iRow.Cells[0].Value.ToString() + "',";  //stock_code
                sSql += "'" + iRow.Cells[1].Value.ToString() + "',";  //monitor_price
                switch (iRow.Cells[2].Value.ToString().Trim())  //direction
                {
                    case "小于":
                        sSql += "'1')";
                        break;
                    case "小于等于":
                        sSql += "'2')";
                        break;
                    case "大于":
                        sSql += "'3')";
                        break;
                    case "大于等于":
                        sSql += "'4')";
                        break;
                    default:
                        sSql += "'0')";
                        break;
                }
                sSql += ";";
            }
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

            RefreshDB();
        }
    }
}
