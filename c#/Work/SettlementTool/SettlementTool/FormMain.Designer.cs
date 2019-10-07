namespace SettlementTool
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
            this.components = new System.ComponentModel.Container();
            this.grbDB = new System.Windows.Forms.GroupBox();
            this.txtDB = new System.Windows.Forms.RichTextBox();
            this.btnConnectDB = new System.Windows.Forms.Button();
            this.grbSettle = new System.Windows.Forms.GroupBox();
            this.label1 = new System.Windows.Forms.Label();
            this.dateDeal = new System.Windows.Forms.DateTimePicker();
            this.txtInfo = new System.Windows.Forms.RichTextBox();
            this.btnRename = new System.Windows.Forms.Button();
            this.btnFormat = new System.Windows.Forms.Button();
            this.btnMail = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.设置ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.券商邮箱设置ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.重命名格式设置ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.邮件收取路径ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.接收邮箱设置ToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.grbDB.SuspendLayout();
            this.grbSettle.SuspendLayout();
            this.menuStrip1.SuspendLayout();
            this.SuspendLayout();
            // 
            // grbDB
            // 
            this.grbDB.Controls.Add(this.txtDB);
            this.grbDB.Controls.Add(this.btnConnectDB);
            this.grbDB.Location = new System.Drawing.Point(26, 46);
            this.grbDB.Name = "grbDB";
            this.grbDB.Size = new System.Drawing.Size(528, 122);
            this.grbDB.TabIndex = 0;
            this.grbDB.TabStop = false;
            this.grbDB.Text = "数据库连接";
            // 
            // txtDB
            // 
            this.txtDB.Font = new System.Drawing.Font("宋体", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.txtDB.Location = new System.Drawing.Point(172, 49);
            this.txtDB.Name = "txtDB";
            this.txtDB.ReadOnly = true;
            this.txtDB.Size = new System.Drawing.Size(336, 34);
            this.txtDB.TabIndex = 1;
            this.txtDB.Text = "";
            // 
            // btnConnectDB
            // 
            this.btnConnectDB.Location = new System.Drawing.Point(38, 49);
            this.btnConnectDB.Name = "btnConnectDB";
            this.btnConnectDB.Size = new System.Drawing.Size(115, 34);
            this.btnConnectDB.TabIndex = 0;
            this.btnConnectDB.Text = "连接数据库";
            this.btnConnectDB.UseVisualStyleBackColor = true;
            this.btnConnectDB.Click += new System.EventHandler(this.btnConnectDB_Click);
            // 
            // grbSettle
            // 
            this.grbSettle.Controls.Add(this.label1);
            this.grbSettle.Controls.Add(this.dateDeal);
            this.grbSettle.Controls.Add(this.txtInfo);
            this.grbSettle.Controls.Add(this.btnRename);
            this.grbSettle.Controls.Add(this.btnFormat);
            this.grbSettle.Controls.Add(this.btnMail);
            this.grbSettle.Location = new System.Drawing.Point(26, 213);
            this.grbSettle.Name = "grbSettle";
            this.grbSettle.Size = new System.Drawing.Size(528, 314);
            this.grbSettle.TabIndex = 1;
            this.grbSettle.TabStop = false;
            this.grbSettle.Text = "结算处理";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(170, 37);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(137, 12);
            this.label1.TabIndex = 5;
            this.label1.Text = "需要处理的数据的日期：";
            // 
            // dateDeal
            // 
            this.dateDeal.Format = System.Windows.Forms.DateTimePickerFormat.Short;
            this.dateDeal.Location = new System.Drawing.Point(308, 34);
            this.dateDeal.Name = "dateDeal";
            this.dateDeal.Size = new System.Drawing.Size(200, 21);
            this.dateDeal.TabIndex = 4;
            this.dateDeal.Value = new System.DateTime(2016, 6, 21, 14, 32, 12, 0);
            // 
            // txtInfo
            // 
            this.txtInfo.Location = new System.Drawing.Point(172, 73);
            this.txtInfo.Name = "txtInfo";
            this.txtInfo.ReadOnly = true;
            this.txtInfo.Size = new System.Drawing.Size(336, 216);
            this.txtInfo.TabIndex = 3;
            this.txtInfo.Text = "";
            // 
            // btnRename
            // 
            this.btnRename.Location = new System.Drawing.Point(38, 225);
            this.btnRename.Name = "btnRename";
            this.btnRename.Size = new System.Drawing.Size(115, 40);
            this.btnRename.TabIndex = 2;
            this.btnRename.Text = "批量重命名";
            this.btnRename.UseVisualStyleBackColor = true;
            // 
            // btnFormat
            // 
            this.btnFormat.Location = new System.Drawing.Point(38, 138);
            this.btnFormat.Name = "btnFormat";
            this.btnFormat.Size = new System.Drawing.Size(115, 40);
            this.btnFormat.TabIndex = 1;
            this.btnFormat.Text = "整理格式";
            this.btnFormat.UseVisualStyleBackColor = true;
            // 
            // btnMail
            // 
            this.btnMail.Location = new System.Drawing.Point(38, 49);
            this.btnMail.Name = "btnMail";
            this.btnMail.Size = new System.Drawing.Size(115, 40);
            this.btnMail.TabIndex = 0;
            this.btnMail.Text = "收取邮件";
            this.btnMail.UseVisualStyleBackColor = true;
            this.btnMail.Click += new System.EventHandler(this.btnMail_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.设置ToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(579, 25);
            this.menuStrip1.TabIndex = 2;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // 设置ToolStripMenuItem
            // 
            this.设置ToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.券商邮箱设置ToolStripMenuItem,
            this.重命名格式设置ToolStripMenuItem,
            this.邮件收取路径ToolStripMenuItem,
            this.接收邮箱设置ToolStripMenuItem});
            this.设置ToolStripMenuItem.Name = "设置ToolStripMenuItem";
            this.设置ToolStripMenuItem.Size = new System.Drawing.Size(44, 21);
            this.设置ToolStripMenuItem.Text = "设置";
            // 
            // 券商邮箱设置ToolStripMenuItem
            // 
            this.券商邮箱设置ToolStripMenuItem.Name = "券商邮箱设置ToolStripMenuItem";
            this.券商邮箱设置ToolStripMenuItem.Size = new System.Drawing.Size(160, 22);
            this.券商邮箱设置ToolStripMenuItem.Text = "券商邮箱设置";
            this.券商邮箱设置ToolStripMenuItem.Click += new System.EventHandler(this.券商邮箱设置ToolStripMenuItem_Click);
            // 
            // 重命名格式设置ToolStripMenuItem
            // 
            this.重命名格式设置ToolStripMenuItem.Name = "重命名格式设置ToolStripMenuItem";
            this.重命名格式设置ToolStripMenuItem.Size = new System.Drawing.Size(160, 22);
            this.重命名格式设置ToolStripMenuItem.Text = "重命名格式设置";
            this.重命名格式设置ToolStripMenuItem.Click += new System.EventHandler(this.重命名格式设置ToolStripMenuItem_Click);
            // 
            // 邮件收取路径ToolStripMenuItem
            // 
            this.邮件收取路径ToolStripMenuItem.Name = "邮件收取路径ToolStripMenuItem";
            this.邮件收取路径ToolStripMenuItem.Size = new System.Drawing.Size(160, 22);
            this.邮件收取路径ToolStripMenuItem.Text = "路径设置";
            this.邮件收取路径ToolStripMenuItem.Click += new System.EventHandler(this.邮件收取路径ToolStripMenuItem_Click);
            // 
            // 接收邮箱设置ToolStripMenuItem
            // 
            this.接收邮箱设置ToolStripMenuItem.Name = "接收邮箱设置ToolStripMenuItem";
            this.接收邮箱设置ToolStripMenuItem.Size = new System.Drawing.Size(160, 22);
            this.接收邮箱设置ToolStripMenuItem.Text = "接收邮箱设置";
            this.接收邮箱设置ToolStripMenuItem.Click += new System.EventHandler(this.接收邮箱设置ToolStripMenuItem_Click);
            // 
            // timer1
            // 
            this.timer1.Enabled = true;
            this.timer1.Interval = 500;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(579, 551);
            this.Controls.Add(this.grbSettle);
            this.Controls.Add(this.grbDB);
            this.Controls.Add(this.menuStrip1);
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "FormMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "结算工具";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.Form1_FormClosed);
            this.Load += new System.EventHandler(this.Form1_Load);
            this.grbDB.ResumeLayout(false);
            this.grbSettle.ResumeLayout(false);
            this.grbSettle.PerformLayout();
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.GroupBox grbDB;
        private System.Windows.Forms.Button btnConnectDB;
        private System.Windows.Forms.GroupBox grbSettle;
        private System.Windows.Forms.Button btnMail;
        private System.Windows.Forms.Button btnRename;
        private System.Windows.Forms.Button btnFormat;
        private System.Windows.Forms.MenuStrip menuStrip1;
        private System.Windows.Forms.ToolStripMenuItem 设置ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem 券商邮箱设置ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem 重命名格式设置ToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem 邮件收取路径ToolStripMenuItem;
        private System.Windows.Forms.RichTextBox txtInfo;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.RichTextBox txtDB;
        private System.Windows.Forms.ToolStripMenuItem 接收邮箱设置ToolStripMenuItem;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.DateTimePicker dateDeal;
    }
}

