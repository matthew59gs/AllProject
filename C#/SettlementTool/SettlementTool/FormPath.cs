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
    public partial class FormPath : Form
    {
        public FormPath()
        {
            InitializeComponent();
        }

        private void btnMainpath_Click(object sender, EventArgs e)
        {
            if (txtMainpath.Text.Trim() != "")
                folderBrowserDialog1.SelectedPath = txtMainpath.Text;
            if (folderBrowserDialog1.ShowDialog() == DialogResult.OK)
                txtMainpath.Text = folderBrowserDialog1.SelectedPath;
        }

        private void FormPath_Load(object sender, EventArgs e)
        {
            RefreshData();
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            string sSql = "delete from pathlist where pathname = 'Main';";
            sSql += "insert into pathlist(pathname, path) values(";
            sSql += "'Main',";
            string newpath = "", oldpath = txtMainpath.Text;
            for (int i = 0; i < oldpath.Length; ++i)
            {
                newpath += oldpath[i];
                if (oldpath[i] == '\\')
                    newpath += @"\";
            }
            sSql += "'" + newpath + "');";
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

        private void RefreshData()
        {
            string sql = "select path from pathlist where pathname = 'Main';";
            MySqlCommand cmd = new MySqlCommand(sql, FormMain.conn);
            MySqlDataAdapter data = new MySqlDataAdapter(cmd);
            DataSet ds = new DataSet();
            data.Fill(ds);
            DataRow iRow = ds.Tables[0].Rows[0];
            txtMainpath.Text = iRow["path"].ToString();
        }
    }
}
