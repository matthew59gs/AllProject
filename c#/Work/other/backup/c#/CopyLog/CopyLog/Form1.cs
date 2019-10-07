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

namespace CopyLog
{
    public partial class FrmMain : Form
    {
        MySqlConnection conn;

        public FrmMain()
        {
            InitializeComponent();
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void FrmMain_Load(object sender, EventArgs e)
        {
            conn = new MySqlConnection("server=192.168.40.202;user id=trader;password=123456;database=tradesplit");
            try
            {

            }
            catch(Exception e)
            {
                MessageBox.Show(e);
            }
        }
    }
}
