namespace FileTrans
{
    partial class FormMain
    {
        /// <summary>
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows 窗体设计器生成的代码

        /// <summary>
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.txtSrc = new System.Windows.Forms.TextBox();
            this.btnSrc = new System.Windows.Forms.Button();
            this.grpSrc = new System.Windows.Forms.GroupBox();
            this.grpDst = new System.Windows.Forms.GroupBox();
            this.txtDst = new System.Windows.Forms.TextBox();
            this.btnDst = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.btnChange = new System.Windows.Forms.Button();
            this.grpSrc.SuspendLayout();
            this.grpDst.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 35);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(71, 12);
            this.label1.TabIndex = 0;
            this.label1.Text = "Oplus文件：";
            // 
            // txtSrc
            // 
            this.txtSrc.Location = new System.Drawing.Point(86, 31);
            this.txtSrc.Name = "txtSrc";
            this.txtSrc.Size = new System.Drawing.Size(126, 21);
            this.txtSrc.TabIndex = 1;
            // 
            // btnSrc
            // 
            this.btnSrc.Location = new System.Drawing.Point(214, 30);
            this.btnSrc.Name = "btnSrc";
            this.btnSrc.Size = new System.Drawing.Size(17, 23);
            this.btnSrc.TabIndex = 2;
            this.btnSrc.Text = ".";
            this.btnSrc.UseVisualStyleBackColor = true;
            this.btnSrc.Click += new System.EventHandler(this.btnSrc_Click);
            // 
            // grpSrc
            // 
            this.grpSrc.Controls.Add(this.txtSrc);
            this.grpSrc.Controls.Add(this.btnSrc);
            this.grpSrc.Controls.Add(this.label1);
            this.grpSrc.Location = new System.Drawing.Point(12, 12);
            this.grpSrc.Name = "grpSrc";
            this.grpSrc.Size = new System.Drawing.Size(260, 80);
            this.grpSrc.TabIndex = 3;
            this.grpSrc.TabStop = false;
            this.grpSrc.Text = "源文件";
            // 
            // grpDst
            // 
            this.grpDst.Controls.Add(this.txtDst);
            this.grpDst.Controls.Add(this.btnDst);
            this.grpDst.Controls.Add(this.label2);
            this.grpDst.Location = new System.Drawing.Point(12, 98);
            this.grpDst.Name = "grpDst";
            this.grpDst.Size = new System.Drawing.Size(260, 80);
            this.grpDst.TabIndex = 4;
            this.grpDst.TabStop = false;
            this.grpDst.Text = "源文件";
            // 
            // txtDst
            // 
            this.txtDst.Location = new System.Drawing.Point(86, 31);
            this.txtDst.Name = "txtDst";
            this.txtDst.Size = new System.Drawing.Size(126, 21);
            this.txtDst.TabIndex = 1;
            // 
            // btnDst
            // 
            this.btnDst.Location = new System.Drawing.Point(214, 30);
            this.btnDst.Name = "btnDst";
            this.btnDst.Size = new System.Drawing.Size(17, 23);
            this.btnDst.TabIndex = 2;
            this.btnDst.Text = ".";
            this.btnDst.UseVisualStyleBackColor = true;
            this.btnDst.Click += new System.EventHandler(this.btnDst_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 35);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(65, 12);
            this.label2.TabIndex = 0;
            this.label2.Text = "CATS文件：";
            // 
            // btnChange
            // 
            this.btnChange.Location = new System.Drawing.Point(62, 203);
            this.btnChange.Name = "btnChange";
            this.btnChange.Size = new System.Drawing.Size(142, 23);
            this.btnChange.TabIndex = 5;
            this.btnChange.Text = "转换";
            this.btnChange.UseVisualStyleBackColor = true;
            this.btnChange.Click += new System.EventHandler(this.btnChange_Click);
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(284, 262);
            this.Controls.Add(this.btnChange);
            this.Controls.Add(this.grpDst);
            this.Controls.Add(this.grpSrc);
            this.Name = "FormMain";
            this.Text = "文件格式转换";
            this.grpSrc.ResumeLayout(false);
            this.grpSrc.PerformLayout();
            this.grpDst.ResumeLayout(false);
            this.grpDst.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtSrc;
        private System.Windows.Forms.Button btnSrc;
        private System.Windows.Forms.GroupBox grpSrc;
        private System.Windows.Forms.GroupBox grpDst;
        private System.Windows.Forms.TextBox txtDst;
        private System.Windows.Forms.Button btnDst;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button btnChange;
    }
}

