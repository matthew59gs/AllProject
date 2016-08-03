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
    public partial class FormMail : Form
    {
        public FormMail()
        {
            InitializeComponent();
        }

        private void FormMail_Load(object sender, EventArgs e)
        {
            gridMail.AllowUserToAddRows = false;
            gridMail.AllowUserToDeleteRows = false;
            gridMail.ReadOnly = true;

            if (FormMain.conn.State != ConnectionState.Open)
                MessageBox.Show("数据库未连接，请先在主窗口中连接数据库！");
            else
                RefreshTable();
        }

        private void btnEdit_Click(object sender, EventArgs e)
        {
            gridMail.AllowUserToAddRows = true;
            gridMail.AllowUserToDeleteRows = true;
            gridMail.ReadOnly = false;
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            gridMail.AllowUserToAddRows = false;
            gridMail.AllowUserToDeleteRows = false;
            gridMail.ReadOnly = true;

            string sSql = "DELETE from maillist;";
            foreach(DataGridViewRow iRow in gridMail.Rows)
            {
                sSql += "insert into maillist(brokername, mailaddress, subject, valid) VALUES(";
                sSql = sSql + "'" + iRow.Cells[0].Value.ToString() + "',";  //Brokername
                sSql = sSql + "'" + iRow.Cells[1].Value.ToString() + "',";  //MailAddress
                sSql = sSql + "'" + iRow.Cells[2].Value.ToString() + "',";  //Subject
                if (iRow.Cells[3].Value.ToString().Trim() != "是")           //Valid
                    sSql = sSql + "'0')";
                else
                    sSql = sSql + "'1')";
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

            RefreshTable();
        }

        // 输出原始数据
        private void RefreshTable()
        {
            string sql = "select brokername as '券商名称', mailaddress as '邮箱地址', subject as '关键字', case valid when '1' then '是' else '否' end as '是否有效' from maillist;";
            MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
            MySqlDataAdapter data = new MySqlDataAdapter(cmd);
            DataSet ds = new DataSet();
            data.Fill(ds);
            gridMail.DataSource = ds.Tables[0];
        }
    }

    public struct BrokerMailInfo
    {
        public string no_pro;               /// 记录编号
        public string brokername_pro;       /// 券商名称
        public string mailaddress_pro;      /// 邮箱地址
        public string subject_pro;          /// 主题关键字
    }

}
