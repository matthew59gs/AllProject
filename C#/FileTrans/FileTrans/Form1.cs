using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace FileTrans
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
        }

        private void btnSrc_Click(object sender, EventArgs e)
        {
            OpenFileDialog fi = new OpenFileDialog();
            if (fi.ShowDialog() == DialogResult.OK)
                txtSrc.Text = fi.FileName;
        }

        private void btnDst_Click(object sender, EventArgs e)
        {
            OpenFileDialog fi = new OpenFileDialog();
            if (fi.ShowDialog() == DialogResult.OK)
                txtDst.Text = fi.FileName;
        }

        private void btnChange_Click(object sender, EventArgs e)
        {
            if (txtSrc.Text.Trim() == "")
            {
                MessageBox.Show("目标文件路径为空");
            }
            FileInfo fi = new FileInfo(txtSrc.Text);
            if (fi.Extension == "xls")
            {

            }
            else if (fi.Extension == "xlsx")
            {

            }
        }

    }
}
