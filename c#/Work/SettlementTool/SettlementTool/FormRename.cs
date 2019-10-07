using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data;
using MySql.Data.MySqlClient;

namespace SettlementTool
{
    public partial class FormRename : Form
    {
        public FormRename()
        {
            InitializeComponent();
        }

        private void FormRename_Load(object sender, EventArgs e)
        {
            gridData.AllowUserToAddRows = false;
            gridData.AllowUserToDeleteRows = false;
            gridData.ReadOnly = true;

            if (FormMain.conn.State != ConnectionState.Open)
                MessageBox.Show("数据库未连接，请先在主窗口中连接数据库！");
            else
                RefreshTable();
        }

        // 输出原始数据
        private void RefreshTable()
        {
            string sql = "select fundcode as '基金代码', fundname as '基金名称', brokercode as '券商代码', oldpattern as '原始文件格式', newpattern as '目标文件格式' from renamelist;";
            MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
            MySqlDataAdapter data = new MySqlDataAdapter(cmd);
            DataSet ds = new DataSet();
            data.Fill(ds);
            gridData.DataSource = ds.Tables[0];
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            gridData.AllowUserToAddRows = true;
            gridData.AllowUserToDeleteRows = true;
            gridData.ReadOnly = false;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            gridData.AllowUserToAddRows = false;
            gridData.AllowUserToDeleteRows = false;
            gridData.ReadOnly = true;

            string sSql = "delete from renamelist;";
            foreach (DataGridViewRow iRow in gridData.Rows)
            {
                sSql += "insert into renamelist(fundcode, fundname, brokercode, oldpattern, newpattern) VALUES(";
                sSql += "'" + iRow.Cells[0].Value.ToString() + "',";  //fundcode
                sSql += "'" + iRow.Cells[1].Value.ToString() + "',";  //fundname
                sSql += "'" + iRow.Cells[2].Value.ToString() + "',";  //brokercode
                sSql += "'" + iRow.Cells[3].Value.ToString() + "',";  //oldpattern
                sSql += "'" + iRow.Cells[4].Value.ToString() + "')";  //newpattern
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

            RefreshTable();
        }
    }

    public struct RenameInfo
    {
        public string fundcode;
        public string fundname;
        public string brokercode;
        public string oldpattern;
        public string newpattern;
    }
}
