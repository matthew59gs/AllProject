using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SettlementTool
{
    public partial class processbar : Form
    {
        public processbar()
        {
            InitializeComponent();
        }

        /// <summary>
        /// 进度条最大值
        /// </summary>
        public int MailCountMax
        {
            get { return progressBar1.Maximum; }
            set { progressBar1.Maximum = value; }
        }

        /// <summary>
        /// 正在处理的邮件编号
        /// </summary>
        public int DealingMailIndex
        {
            get { return progressBar1.Value; }
            set { progressBar1.Value = value; }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (progressBar1.Value == progressBar1.Maximum)
            {
                label1.Text = "全部" + progressBar1.Maximum.ToString() + "封邮件已经收取完毕";
                btnOK.Enabled = true;
            }
            else
                label1.Text = "正在接收第" + progressBar1.Value.ToString() + "封邮件...";
        }

        private void processbar_Load(object sender, EventArgs e)
        {
            progressBar1.Minimum = 1;
            btnOK.Enabled = false;
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            Close();
        }

        public void Stop()
        {
            label1.Text = "接收邮件出现异常，接收中止";
            btnOK.Enabled = true;
        }
    }
}
