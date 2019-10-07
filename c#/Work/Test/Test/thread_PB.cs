using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Test
{
    public partial class thread_PB : Form
    {
        public thread_PB(int iMax)
        {
            InitializeComponent();
            progressBar1.Maximum = iMax;
            label1.Text = "正在接收第0/" + iMax.ToString() + "封邮件";
        }

        public bool increase(int iValue)
        {
            if (iValue > 0)
            {
                if(progressBar1.Value + iValue < progressBar1.Maximum)
                {
                    progressBar1.Value += iValue;
                    label1.Text = "正在接收第" + progressBar1.Value.ToString() + "/" + progressBar1.Maximum.ToString() + "封邮件";
                    Application.DoEvents();
                    progressBar1.Update();
                    progressBar1.Refresh();
                    return true;
                }
                else
                {
                    progressBar1.Value = progressBar1.Maximum;
                    this.Close();//执行完之后，自动关闭子窗体
                    return false;
                }
            }
            return false;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}
