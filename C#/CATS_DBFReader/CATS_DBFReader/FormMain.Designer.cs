namespace CATS_DBFReader
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
            this.btnLink = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.txtPath = new System.Windows.Forms.TextBox();
            this.btnBrowse = new System.Windows.Forms.Button();
            this.grpDBFLocate = new System.Windows.Forms.GroupBox();
            this.dataGridData = new System.Windows.Forms.DataGridView();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.grpDBFLocate.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridData)).BeginInit();
            this.SuspendLayout();
            // 
            // btnLink
            // 
            this.btnLink.Location = new System.Drawing.Point(310, 47);
            this.btnLink.Name = "btnLink";
            this.btnLink.Size = new System.Drawing.Size(75, 23);
            this.btnLink.TabIndex = 0;
            this.btnLink.Text = "连接";
            this.btnLink.UseVisualStyleBackColor = true;
            this.btnLink.Click += new System.EventHandler(this.btnLink_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(8, 52);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(83, 12);
            this.label1.TabIndex = 1;
            this.label1.Text = "DBF文件位置：";
            // 
            // txtPath
            // 
            this.txtPath.Location = new System.Drawing.Point(97, 48);
            this.txtPath.Name = "txtPath";
            this.txtPath.Size = new System.Drawing.Size(164, 21);
            this.txtPath.TabIndex = 2;
            // 
            // btnBrowse
            // 
            this.btnBrowse.Location = new System.Drawing.Point(263, 47);
            this.btnBrowse.Name = "btnBrowse";
            this.btnBrowse.Size = new System.Drawing.Size(20, 23);
            this.btnBrowse.TabIndex = 3;
            this.btnBrowse.Text = ".";
            this.btnBrowse.UseVisualStyleBackColor = true;
            this.btnBrowse.Click += new System.EventHandler(this.btnBrowse_Click);
            // 
            // grpDBFLocate
            // 
            this.grpDBFLocate.Controls.Add(this.txtPath);
            this.grpDBFLocate.Controls.Add(this.btnBrowse);
            this.grpDBFLocate.Controls.Add(this.btnLink);
            this.grpDBFLocate.Controls.Add(this.label1);
            this.grpDBFLocate.Location = new System.Drawing.Point(12, 12);
            this.grpDBFLocate.Name = "grpDBFLocate";
            this.grpDBFLocate.Size = new System.Drawing.Size(428, 117);
            this.grpDBFLocate.TabIndex = 4;
            this.grpDBFLocate.TabStop = false;
            this.grpDBFLocate.Text = "DBF文件";
            // 
            // dataGridData
            // 
            this.dataGridData.AllowUserToAddRows = false;
            this.dataGridData.AllowUserToDeleteRows = false;
            this.dataGridData.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridData.Location = new System.Drawing.Point(13, 147);
            this.dataGridData.Name = "dataGridData";
            this.dataGridData.ReadOnly = true;
            this.dataGridData.RowTemplate.Height = 23;
            this.dataGridData.Size = new System.Drawing.Size(427, 246);
            this.dataGridData.TabIndex = 5;
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
            this.ClientSize = new System.Drawing.Size(452, 405);
            this.Controls.Add(this.dataGridData);
            this.Controls.Add(this.grpDBFLocate);
            this.Name = "FormMain";
            this.Text = "DBFReader";
            this.grpDBFLocate.ResumeLayout(false);
            this.grpDBFLocate.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridData)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button btnLink;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox txtPath;
        private System.Windows.Forms.Button btnBrowse;
        private System.Windows.Forms.GroupBox grpDBFLocate;
        private System.Windows.Forms.DataGridView dataGridData;
        private System.Windows.Forms.Timer timer1;
    }
}

