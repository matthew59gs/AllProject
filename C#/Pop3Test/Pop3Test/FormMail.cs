using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using UtilSp.ClassLib;

namespace Pop3Test
{
    public partial class FormMail : Form
    {
        public FormMail()
        {
            InitializeComponent();
        }

        #region mail normal Property
        private string mail_ = "";
        public string mail_pro
        {
            get
            {
                return mail_;
            }
            set
            {
                mail_ = value;
            }
        }
        #endregion

        private void FormMail_Load(object sender, EventArgs e)
        {
            textBoxMail.Text = mail_pro;
        }

        private void saveToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string saveName = FileSp.getSaveDialogFileName("Save", "All Files|*.*|Email|*.eml", 2);
            if (string.IsNullOrEmpty(saveName))
            {
                return;
            }
            bool isSaveOK = FileSp.writeStringToFile(saveName, textBoxMail.Text, true);
            if (isSaveOK)
            {
                MessageBox.Show(Tip.saveOK);
            }
            else
            {
                string failMessage = Tip.saveFail;
                if (FileSp.exception_pro != null)
                {
                    failMessage += FileSp.exception_pro.Message;
                }
                MessageBox.Show(failMessage);
            }
        }

        private class Tip
        {
            public static string saveOK = "Save OK!";
            public static string saveFail = "Save Fail!";
            public static string copyOK = "Has copy to clipboard!";
        }

        private void selectAllToolStripMenuItem_Click(object sender, EventArgs e)
        {
            textBoxMail.SelectAll();
        }

        private void copyToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Clipboard.SetText(textBoxMail.SelectedText);
            toolTipInfo.Show(Tip.copyOK, textBoxMail);
        }
    }
}
