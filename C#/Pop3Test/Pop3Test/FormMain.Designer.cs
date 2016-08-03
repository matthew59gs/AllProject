namespace Pop3Test
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
        /// 设计器支持所需的方法 - 不要
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormMain));
            this.label1 = new System.Windows.Forms.Label();
            this.textBoxHost = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.textBoxPort = new System.Windows.Forms.TextBox();
            this.buttonConnect = new System.Windows.Forms.Button();
            this.buttonDisconnect = new System.Windows.Forms.Button();
            this.groupBoxConnect = new System.Windows.Forms.GroupBox();
            this.buttonFetch = new System.Windows.Forms.Button();
            this.groupBoxInfo = new System.Windows.Forms.GroupBox();
            this.panelInfoSet = new System.Windows.Forms.Panel();
            this.dataGridViewMail = new System.Windows.Forms.DataGridView();
            this.Index = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Column1 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.From = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Subject = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Summary = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Body = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.panelMailListInfo = new System.Windows.Forms.Panel();
            this.buttonNext = new System.Windows.Forms.Button();
            this.buttonPrevious = new System.Windows.Forms.Button();
            this.textBoxMailCount = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.panelTool = new System.Windows.Forms.Panel();
            this.label4 = new System.Windows.Forms.Label();
            this.textBoxPassword = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.textBoxUserName = new System.Windows.Forms.TextBox();
            this.buttonStatusInfo = new System.Windows.Forms.Button();
            this.toolTipInfo = new System.Windows.Forms.ToolTip(this.components);
            this.buttonSsl = new System.Windows.Forms.Button();
            this.checkBoxUseSSL = new System.Windows.Forms.CheckBox();
            this.groupBoxConnect.SuspendLayout();
            this.groupBoxInfo.SuspendLayout();
            this.panelInfoSet.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewMail)).BeginInit();
            this.panelMailListInfo.SuspendLayout();
            this.panelTool.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(38, 25);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(35, 12);
            this.label1.TabIndex = 0;
            this.label1.Text = "Host:";
            // 
            // textBoxHost
            // 
            this.textBoxHost.Location = new System.Drawing.Point(79, 20);
            this.textBoxHost.Name = "textBoxHost";
            this.textBoxHost.Size = new System.Drawing.Size(246, 21);
            this.textBoxHost.TabIndex = 1;
            this.textBoxHost.Text = "pop.qq.com";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(369, 25);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(35, 12);
            this.label2.TabIndex = 2;
            this.label2.Text = "Port:";
            // 
            // textBoxPort
            // 
            this.textBoxPort.Location = new System.Drawing.Point(410, 22);
            this.textBoxPort.Name = "textBoxPort";
            this.textBoxPort.Size = new System.Drawing.Size(151, 21);
            this.textBoxPort.TabIndex = 3;
            this.textBoxPort.Text = "110";
            // 
            // buttonConnect
            // 
            this.buttonConnect.Location = new System.Drawing.Point(667, 16);
            this.buttonConnect.Name = "buttonConnect";
            this.buttonConnect.Size = new System.Drawing.Size(117, 39);
            this.buttonConnect.TabIndex = 4;
            this.buttonConnect.Text = "Connect";
            this.buttonConnect.UseVisualStyleBackColor = true;
            this.buttonConnect.Click += new System.EventHandler(this.buttonConnect_Click);
            // 
            // buttonDisconnect
            // 
            this.buttonDisconnect.Location = new System.Drawing.Point(851, 16);
            this.buttonDisconnect.Name = "buttonDisconnect";
            this.buttonDisconnect.Size = new System.Drawing.Size(117, 39);
            this.buttonDisconnect.TabIndex = 5;
            this.buttonDisconnect.Text = "Disconnect";
            this.buttonDisconnect.UseVisualStyleBackColor = true;
            this.buttonDisconnect.Click += new System.EventHandler(this.buttonDisconnect_Click);
            // 
            // groupBoxConnect
            // 
            this.groupBoxConnect.Controls.Add(this.checkBoxUseSSL);
            this.groupBoxConnect.Controls.Add(this.textBoxHost);
            this.groupBoxConnect.Controls.Add(this.label1);
            this.groupBoxConnect.Controls.Add(this.label2);
            this.groupBoxConnect.Controls.Add(this.textBoxPort);
            this.groupBoxConnect.Controls.Add(this.buttonConnect);
            this.groupBoxConnect.Controls.Add(this.buttonDisconnect);
            this.groupBoxConnect.Dock = System.Windows.Forms.DockStyle.Top;
            this.groupBoxConnect.Location = new System.Drawing.Point(0, 0);
            this.groupBoxConnect.Name = "groupBoxConnect";
            this.groupBoxConnect.Size = new System.Drawing.Size(1020, 61);
            this.groupBoxConnect.TabIndex = 12;
            this.groupBoxConnect.TabStop = false;
            this.groupBoxConnect.Text = "Connect";         
            // 
            // buttonFetch
            // 
            this.buttonFetch.Location = new System.Drawing.Point(582, 4);
            this.buttonFetch.Name = "buttonFetch";
            this.buttonFetch.Size = new System.Drawing.Size(396, 39);
            this.buttonFetch.TabIndex = 16;
            this.buttonFetch.Text = "Fetch";
            this.buttonFetch.UseVisualStyleBackColor = true;
            this.buttonFetch.Click += new System.EventHandler(this.buttonFetch_Click);
            // 
            // groupBoxInfo
            // 
            this.groupBoxInfo.Controls.Add(this.panelInfoSet);
            this.groupBoxInfo.Controls.Add(this.buttonStatusInfo);
            this.groupBoxInfo.Dock = System.Windows.Forms.DockStyle.Fill;
            this.groupBoxInfo.Location = new System.Drawing.Point(0, 61);
            this.groupBoxInfo.Name = "groupBoxInfo";
            this.groupBoxInfo.Size = new System.Drawing.Size(1020, 434);
            this.groupBoxInfo.TabIndex = 14;
            this.groupBoxInfo.TabStop = false;
            this.groupBoxInfo.Text = "Info";
            // 
            // panelInfoSet
            // 
            this.panelInfoSet.Controls.Add(this.dataGridViewMail);
            this.panelInfoSet.Controls.Add(this.panelMailListInfo);
            this.panelInfoSet.Controls.Add(this.panelTool);
            this.panelInfoSet.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelInfoSet.Location = new System.Drawing.Point(3, 17);
            this.panelInfoSet.Name = "panelInfoSet";
            this.panelInfoSet.Size = new System.Drawing.Size(1014, 347);
            this.panelInfoSet.TabIndex = 11;
            // 
            // dataGridViewMail
            // 
            this.dataGridViewMail.AllowUserToAddRows = false;
            this.dataGridViewMail.BackgroundColor = System.Drawing.Color.White;
            this.dataGridViewMail.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewMail.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Index,
            this.Column1,
            this.From,
            this.Subject,
            this.Summary,
            this.Body});
            this.dataGridViewMail.Dock = System.Windows.Forms.DockStyle.Fill;
            this.dataGridViewMail.GridColor = System.Drawing.SystemColors.WindowFrame;
            this.dataGridViewMail.Location = new System.Drawing.Point(0, 107);
            this.dataGridViewMail.Name = "dataGridViewMail";
            this.dataGridViewMail.RowTemplate.Height = 23;
            this.dataGridViewMail.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.dataGridViewMail.Size = new System.Drawing.Size(1014, 240);
            this.dataGridViewMail.TabIndex = 20;
            this.dataGridViewMail.CellDoubleClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dataGridViewMail_CellDoubleClick);
            // 
            // Index
            // 
            this.Index.DataPropertyName = "index_pro";
            this.Index.HeaderText = "Index";
            this.Index.Name = "Index";
            this.Index.ReadOnly = true;
            // 
            // Column1
            // 
            this.Column1.DataPropertyName = "id_pro";
            this.Column1.HeaderText = "ID";
            this.Column1.Name = "Column1";
            this.Column1.ReadOnly = true;
            this.Column1.Visible = false;
            // 
            // From
            // 
            this.From.DataPropertyName = "from_pro";
            this.From.HeaderText = "From";
            this.From.Name = "From";
            this.From.ReadOnly = true;
            this.From.Width = 150;
            // 
            // Subject
            // 
            this.Subject.DataPropertyName = "subject_pro";
            this.Subject.HeaderText = "Subject";
            this.Subject.Name = "Subject";
            this.Subject.ReadOnly = true;
            this.Subject.Width = 400;
            // 
            // Summary
            // 
            this.Summary.DataPropertyName = "summary_pro";
            this.Summary.HeaderText = "Summary";
            this.Summary.Name = "Summary";
            this.Summary.ReadOnly = true;
            this.Summary.Visible = false;
            // 
            // Body
            // 
            this.Body.DataPropertyName = "body_pro";
            this.Body.HeaderText = "Body";
            this.Body.Name = "Body";
            this.Body.Visible = false;
            // 
            // panelMailListInfo
            // 
            this.panelMailListInfo.Controls.Add(this.buttonSsl);
            this.panelMailListInfo.Controls.Add(this.buttonNext);
            this.panelMailListInfo.Controls.Add(this.buttonPrevious);
            this.panelMailListInfo.Controls.Add(this.textBoxMailCount);
            this.panelMailListInfo.Controls.Add(this.label5);
            this.panelMailListInfo.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelMailListInfo.Location = new System.Drawing.Point(0, 53);
            this.panelMailListInfo.Name = "panelMailListInfo";
            this.panelMailListInfo.Size = new System.Drawing.Size(1014, 54);
            this.panelMailListInfo.TabIndex = 21;
            // 
            // buttonNext
            // 
            this.buttonNext.Location = new System.Drawing.Point(733, 7);
            this.buttonNext.Name = "buttonNext";
            this.buttonNext.Size = new System.Drawing.Size(117, 39);
            this.buttonNext.TabIndex = 20;
            this.buttonNext.Text = "Next";
            this.buttonNext.UseVisualStyleBackColor = true;
            this.buttonNext.Click += new System.EventHandler(this.buttonNext_Click);
            // 
            // buttonPrevious
            // 
            this.buttonPrevious.Location = new System.Drawing.Point(582, 7);
            this.buttonPrevious.Name = "buttonPrevious";
            this.buttonPrevious.Size = new System.Drawing.Size(117, 39);
            this.buttonPrevious.TabIndex = 19;
            this.buttonPrevious.Text = "Previous";
            this.buttonPrevious.UseVisualStyleBackColor = true;
            this.buttonPrevious.Click += new System.EventHandler(this.buttonPrevious_Click);
            // 
            // textBoxMailCount
            // 
            this.textBoxMailCount.Location = new System.Drawing.Point(76, 17);
            this.textBoxMailCount.Name = "textBoxMailCount";
            this.textBoxMailCount.ReadOnly = true;
            this.textBoxMailCount.Size = new System.Drawing.Size(482, 21);
            this.textBoxMailCount.TabIndex = 18;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(5, 20);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(65, 12);
            this.label5.TabIndex = 18;
            this.label5.Text = "MailCount:";
            // 
            // panelTool
            // 
            this.panelTool.Controls.Add(this.buttonFetch);
            this.panelTool.Controls.Add(this.label4);
            this.panelTool.Controls.Add(this.textBoxPassword);
            this.panelTool.Controls.Add(this.label3);
            this.panelTool.Controls.Add(this.textBoxUserName);
            this.panelTool.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelTool.Location = new System.Drawing.Point(0, 0);
            this.panelTool.Name = "panelTool";
            this.panelTool.Size = new System.Drawing.Size(1014, 53);
            this.panelTool.TabIndex = 8;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(342, 17);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(59, 12);
            this.label4.TabIndex = 8;
            this.label4.Text = "Password:";
            // 
            // textBoxPassword
            // 
            this.textBoxPassword.Location = new System.Drawing.Point(407, 14);
            this.textBoxPassword.Name = "textBoxPassword";
            this.textBoxPassword.PasswordChar = '*';
            this.textBoxPassword.Size = new System.Drawing.Size(151, 21);
            this.textBoxPassword.TabIndex = 9;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(11, 14);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(59, 12);
            this.label3.TabIndex = 6;
            this.label3.Text = "UserName:";
            // 
            // textBoxUserName
            // 
            this.textBoxUserName.Location = new System.Drawing.Point(76, 11);
            this.textBoxUserName.Name = "textBoxUserName";
            this.textBoxUserName.Size = new System.Drawing.Size(246, 21);
            this.textBoxUserName.TabIndex = 7;
            // 
            // buttonStatusInfo
            // 
            this.buttonStatusInfo.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.buttonStatusInfo.FlatAppearance.BorderColor = System.Drawing.SystemColors.ControlLight;
            this.buttonStatusInfo.FlatAppearance.MouseDownBackColor = System.Drawing.SystemColors.Control;
            this.buttonStatusInfo.FlatAppearance.MouseOverBackColor = System.Drawing.SystemColors.Control;
            this.buttonStatusInfo.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonStatusInfo.Font = new System.Drawing.Font("宋体", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(134)));
            this.buttonStatusInfo.Location = new System.Drawing.Point(3, 364);
            this.buttonStatusInfo.Name = "buttonStatusInfo";
            this.buttonStatusInfo.Size = new System.Drawing.Size(1014, 67);
            this.buttonStatusInfo.TabIndex = 12;
            this.buttonStatusInfo.UseVisualStyleBackColor = true;
            // 
            // buttonSsl
            // 
            this.buttonSsl.Location = new System.Drawing.Point(887, 14);
            this.buttonSsl.Name = "buttonSsl";
            this.buttonSsl.Size = new System.Drawing.Size(91, 34);
            this.buttonSsl.TabIndex = 17;
            this.buttonSsl.Text = "SSL";
            this.buttonSsl.UseVisualStyleBackColor = true;
            this.buttonSsl.Click += new System.EventHandler(this.buttonSsl_Click);
            // 
            // checkBoxUseSSL
            // 
            this.checkBoxUseSSL.AutoSize = true;
            this.checkBoxUseSSL.Location = new System.Drawing.Point(585, 28);
            this.checkBoxUseSSL.Name = "checkBoxUseSSL";
            this.checkBoxUseSSL.Size = new System.Drawing.Size(60, 16);
            this.checkBoxUseSSL.TabIndex = 13;
            this.checkBoxUseSSL.Text = "UseSSL";
            this.checkBoxUseSSL.UseVisualStyleBackColor = true;
            // 
            // FormMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1020, 495);
            this.Controls.Add(this.groupBoxInfo);
            this.Controls.Add(this.groupBoxConnect);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "FormMain";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Mail_POP3";
            this.Load += new System.EventHandler(this.FormMain_Load);
            this.groupBoxConnect.ResumeLayout(false);
            this.groupBoxConnect.PerformLayout();
            this.groupBoxInfo.ResumeLayout(false);
            this.panelInfoSet.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewMail)).EndInit();
            this.panelMailListInfo.ResumeLayout(false);
            this.panelMailListInfo.PerformLayout();
            this.panelTool.ResumeLayout(false);
            this.panelTool.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBoxHost;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox textBoxPort;
        private System.Windows.Forms.Button buttonConnect;
        private System.Windows.Forms.Button buttonDisconnect;
        private System.Windows.Forms.GroupBox groupBoxConnect;
        private System.Windows.Forms.GroupBox groupBoxInfo;
        private System.Windows.Forms.Panel panelInfoSet;
        private System.Windows.Forms.ToolTip toolTipInfo;
        private System.Windows.Forms.Button buttonFetch;
        private System.Windows.Forms.Button buttonStatusInfo;
        private System.Windows.Forms.Panel panelTool;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox textBoxUserName;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.TextBox textBoxPassword;
        private System.Windows.Forms.DataGridView dataGridViewMail;
        private System.Windows.Forms.Panel panelMailListInfo;
        private System.Windows.Forms.TextBox textBoxMailCount;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.DataGridViewTextBoxColumn Index;
        private System.Windows.Forms.DataGridViewTextBoxColumn Column1;
        private System.Windows.Forms.DataGridViewTextBoxColumn From;
        private System.Windows.Forms.DataGridViewTextBoxColumn Subject;
        private System.Windows.Forms.DataGridViewTextBoxColumn Summary;
        private System.Windows.Forms.DataGridViewTextBoxColumn Body;
        private System.Windows.Forms.Button buttonNext;
        private System.Windows.Forms.Button buttonPrevious;
        private System.Windows.Forms.Button buttonSsl;
        private System.Windows.Forms.CheckBox checkBoxUseSSL;
    }
}

