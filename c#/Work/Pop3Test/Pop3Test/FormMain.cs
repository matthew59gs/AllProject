using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net.Sockets;
using UtilSp.ClassLib;
using System.Linq.Expressions;
using System.Threading;
using System.Security;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Net.Security;
using System.Text.RegularExpressions;

namespace Pop3Test
{
    public partial class FormMain : Form
    {
        public FormMain()
        {
            InitializeComponent();
        }


        private Helper helper_ = new Helper();
        private int beginMailIndex_ = 1;
        private int mailCountPerPage_ = 10;
        private int endMailIndex_ = 10;


        private Pop3Sp pop3sp_ = null;

        private void buttonConnect_Click(object sender, EventArgs e)
        {
            try
            {
                string host = textBoxHost.Text;
                string port = textBoxPort.Text;
                if (string.IsNullOrEmpty(host))
                {
                    showMessage(Tip.hostEmpty);
                    return;
                }

                if (string.IsNullOrEmpty(port))
                {
                    showMessage(Tip.portEmpty);
                    return;
                }

                if (!IpPortSp.isPort(port))
                {
                    MessageBox.Show(Tip.portIllegal);
                    return;
                }

                if (pop3sp_ == null)
                {
                    pop3sp_ = new Pop3Sp();
                }
                pop3sp_.isSsl_pro = checkBoxUseSSL.Checked;
                this.helper_.statusInfo_pro = Tip.connecting;
                this.Refresh();
                enabledWorkArea(false);
                Thread connectThread = new Thread(() =>
                {
                    bool isConnect = pop3sp_.connect(host, Convert.ToInt32(port));
                    this.Invoke((Action)(() =>
                    {
                        if (!isConnect)
                        {
                            showStatusInfo(Tip.connectFail + pop3sp_.getExceptionStr());
                            enabledWorkArea(true);
                            return;
                        }
                        helper_.connectEnabled_pro = false;
                        helper_.disconnectEnabled_pro = true;
                        helper_.fetchEnabled_pro = true;
                        showStatusInfo(Tip.connectOK);
                        enabledWorkArea(true);
                    }));

                });
                connectThread.IsBackground = true;
                connectThread.Start();
            }
            catch (System.Exception ex)
            {
                showStatusInfo(ex.Message);
            }
        }

        private void showMessage(string message)
        {
            MessageBox.Show(message);
        }

        private void showStatusInfo(string statusInfo, bool isNeedInvoke = false)
        {
            if (isNeedInvoke)
            {
                this.Invoke((Action)(() =>
                {
                    helper_.statusInfo_pro = statusInfo + "\r\n";
                }));
            }
            else
            {
                helper_.statusInfo_pro = statusInfo + "\r\n";
            }
        }

        public class Helper : INotifyPropertyChanged
        {
            #region backInfo NotifyPropertyChanged
            public void NotifyPropertyChanged<T>(Expression<Func<T>> property)
            {
                if (PropertyChanged == null)
                {
                    return;
                }
                var memberExpression = property.Body as MemberExpression;
                if (memberExpression == null)
                {
                    return;
                }

                PropertyChanged.Invoke(this, new PropertyChangedEventArgs(memberExpression.Member.Name));
            }

            public event PropertyChangedEventHandler PropertyChanged;
            #endregion

            #region connectEnabled Property
            private bool connectEnabled_ = true;
            public bool connectEnabled_pro
            {
                get
                {
                    return connectEnabled_;
                }
                set
                {

                    if (value == connectEnabled_)
                    {
                        return;
                    }
                    connectEnabled_ = value;
                    NotifyPropertyChanged(() => connectEnabled_pro);
                }
            }
            #endregion

            #region disconnectEnabled Property
            private bool disconnectEnabled_ = false;
            public bool disconnectEnabled_pro
            {
                get
                {
                    return disconnectEnabled_;
                }
                set
                {

                    if (value == disconnectEnabled_)
                    {
                        return;
                    }
                    disconnectEnabled_ = value;
                    NotifyPropertyChanged(() => disconnectEnabled_pro);
                }
            }
            #endregion

            #region fetchEnabled Property
            private bool fetchEnabled_ = false;
            public bool fetchEnabled_pro
            {
                get
                {
                    return fetchEnabled_;
                }
                set
                {

                    if (value == fetchEnabled_)
                    {
                        return;
                    }
                    fetchEnabled_ = value;
                    NotifyPropertyChanged(() => fetchEnabled_pro);
                }
            }
            #endregion

            #region mailCount Property
            private int mailCount_ = 0;
            public int mailCount_pro
            {
                get
                {
                    return mailCount_;
                }
                set
                {

                    if (value == mailCount_)
                    {
                        return;
                    }
                    mailCount_ = value;
                    NotifyPropertyChanged(() => mailCount_pro);
                }
            }
            #endregion

            #region nextEnabled Property
            private bool nextEnabled_ = false;
            public bool nextEnabled_pro
            {
                get
                {
                    return nextEnabled_;
                }
                set
                {

                    if (value == nextEnabled_)
                    {
                        return;
                    }
                    nextEnabled_ = value;
                    NotifyPropertyChanged(() => nextEnabled_pro);
                }
            }
            #endregion

            #region previousEnabled Property
            private bool previousEnabled_ = false;
            public bool previousEnabled_pro
            {
                get
                {
                    return previousEnabled_;
                }
                set
                {

                    if (value == previousEnabled_)
                    {
                        return;
                    }
                    previousEnabled_ = value;
                    NotifyPropertyChanged(() => previousEnabled_pro);
                }
            }
            #endregion

            #region statusInfo Property
            private string statusInfo_ = "";
            public string statusInfo_pro
            {
                get
                {
                    return statusInfo_;
                }
                set
                {

                    if (value == statusInfo_)
                    {
                        return;
                    }
                    statusInfo_ = value;
                    NotifyPropertyChanged(() => statusInfo_pro);
                }
            }
            #endregion
        }

        private void FormMain_Load(object sender, EventArgs e)
        {
            initializeUI();
            binding();
        }

        private void binding()
        {
            buttonStatusInfo.DataBindings.Add("Text", helper_, "statusInfo_pro");
            buttonConnect.DataBindings.Add("Enabled", helper_, "connectEnabled_pro");
            buttonDisconnect.DataBindings.Add("Enabled", helper_, "disconnectEnabled_pro");
            buttonFetch.DataBindings.Add("Enabled", helper_, "fetchEnabled_pro");
            buttonPrevious.DataBindings.Add("Enabled", helper_, "previousEnabled_pro");
            buttonNext.DataBindings.Add("Enabled", helper_, "nextEnabled_pro");
            textBoxMailCount.DataBindings.Add("Text", helper_, "mailCount_pro");
        }

        private void initializeUI()
        {

        }

        private void buttonDisconnect_Click(object sender, EventArgs e)
        {
            try
            {
                if (!pop3sp_.disconnect())
                {
                    this.showStatusInfo(Tip.disconnectFail + pop3sp_.getExceptionStr());
                }
                else
                {
                    helper_.connectEnabled_pro = true;
                    helper_.disconnectEnabled_pro = false;
                    helper_.fetchEnabled_pro = false;
                    this.showStatusInfo(Tip.disconnectOK);
                }

            }
            catch (System.Exception ex)
            {
                this.showStatusInfo(ex.Message);
            }
        }


        private class Tip
        {
            public static string base64ToNormalTip = "Convert base64 string that selected in the info to normal string with encode.Then auto copy result to clipboard.";
            public static string connecting = "Connecting...";
            public static string connectOK = "Connect OK!";
            public static string connectFail = "Connect Fail!";
            public static string disconnectOK = "Disconnect OK!";
            public static string disconnectFail = "Disconnect Fail!";
            public static string fetching = "Fetching...";
            public static string fetched = "Fetch completed!";
            public static string fetchFail = "Fetch mail fail!";
            public static string hostEmpty = "Host is empty!";
            public static string loginFail = "Login Fail!";
            public static string logining = "Logining...";
            public static string loginOK = "Login OK!";
            public static string noMailContent = "No mail content!";
            public static string notConnect = "Not connect!";
            public static string passwordEmpty = "Password is empty!";
            public static string portEmpty = "Port is empty!";
            public static string portIllegal = "Port is illegal!";
            public static string userNameEmpty = "User name is empty!";
        }


        private void buttonFetch_Click(object sender, EventArgs e)
        {
            string userName = textBoxUserName.Text;
            string password = textBoxPassword.Text;
            if (string.IsNullOrEmpty(userName))
            {
                MessageBox.Show(Tip.userNameEmpty);
                return;
            }
            if (string.IsNullOrEmpty(password))
            {
                MessageBox.Show(Tip.passwordEmpty);
                return;
            }
            this.helper_.statusInfo_pro = Tip.logining;
            this.Refresh();
            enabledWorkArea(false);
            Thread fetchThread = new Thread(() =>
            {
                bool isLoginOK = pop3sp_.login(userName, password);
                this.Invoke((Action)(() =>
                {
                    if (!isLoginOK)
                    {
                        if (pop3sp_.exception_pro != null)
                        {
                            this.helper_.statusInfo_pro = Tip.loginFail + pop3sp_.exception_pro.Message;
                        }
                        else
                        {
                            this.helper_.statusInfo_pro = Tip.loginFail;
                        }
                        return;
                    }
                    this.helper_.statusInfo_pro = Tip.loginOK;
                    this.helper_.statusInfo_pro = Tip.fetching;
                    this.helper_.fetchEnabled_pro = false;
                    this.helper_.mailCount_pro = pop3sp_.fetchMailCount();
                    if (this.helper_.mailCount_pro < 0)
                    {
                        if (pop3sp_.exception_pro != null)
                        {
                            this.helper_.statusInfo_pro = Tip.fetchFail + pop3sp_.exception_pro.Message;
                        }
                        else
                        {
                            this.helper_.statusInfo_pro = Tip.fetchFail;
                        }
                        return;
                    }
                    beginMailIndex_ -= mailCountPerPage_;
                    endMailIndex_ -= mailCountPerPage_;
                    fetchMailPage(true);
                    enabledWorkArea(true);
                }));
            });
            fetchThread.IsBackground = true;
            fetchThread.Start();
        }

        private void enabledPageTurn()
        {
            this.helper_.previousEnabled_pro = beginMailIndex_ - mailCountPerPage_ > 0;
            this.helper_.nextEnabled_pro = endMailIndex_ <= this.helper_.mailCount_pro;
        }

        private void fetchMailPage(bool isFetchNext)
        {
            Thread fetchMailThread = new Thread(() =>
            {
                this.Invoke((Action)(() =>
                {
                    this.helper_.statusInfo_pro = Tip.fetching;
                    this.helper_.previousEnabled_pro = false;
                    this.helper_.nextEnabled_pro = false;
                }));

                if (isFetchNext && endMailIndex_ >= this.helper_.mailCount_pro)
                {
                    return;
                }
                else if (!isFetchNext && beginMailIndex_ - mailCountPerPage_ <= 0)
                {
                    return;
                }

                int beginMailIndex = 0;
                int endMailIndex = 0;
                if (isFetchNext)
                {
                    beginMailIndex = beginMailIndex_ + mailCountPerPage_;
                    endMailIndex = endMailIndex_ + mailCountPerPage_;
                    if (endMailIndex_ > this.helper_.mailCount_pro)//Left mail count is less than mailCountPerPage_.
                    {
                        endMailIndex_ = this.helper_.mailCount_pro;
                    }
                }
                else
                {
                    beginMailIndex = beginMailIndex_ - mailCountPerPage_;
                    endMailIndex = endMailIndex_ - mailCountPerPage_;
                }

                List<MailSp> mailList = pop3sp_.fetchMailList(beginMailIndex, endMailIndex);
                if (mailList == null && pop3sp_.exception_pro != null)
                {
                    this.Invoke((Action)(() =>
                    {
                        this.helper_.statusInfo_pro = pop3sp_.exception_pro.Message;
                     }));
                    return;
                }
                this.Invoke((Action)(() =>
                {
                    dataGridViewMail.DataSource = mailList;
                    if (pop3sp_.exception_pro != null)
                    {
                        this.helper_.statusInfo_pro = Tip.fetched + pop3sp_.exception_pro.Message;
                    }
                    else
                    {
                        this.helper_.statusInfo_pro = Tip.fetched;
                        beginMailIndex_ = beginMailIndex;
                        endMailIndex_ = endMailIndex;
                        enabledPageTurn();
                    }
                }));
            });
            fetchMailThread.IsBackground = true;
            fetchMailThread.Start();
        }

        private void buttonTest_Click(object sender, EventArgs e)
        {
            string testStr = "=B4=F7=BB=C0=C8=DD=A3=AC=D6=A7=B8=B6=B1=A6=B5=E7";
            Encoding encoding = Encoding.ASCII; //Encoding.GetEncoding("GBK");
            string result = Base64Sp.toNormalStr(testStr, encoding);
            MessageBox.Show(result);
        }

        private void dataGridViewMail_CellDoubleClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0 || e.ColumnIndex < 0)
            {
                return;
            }
            int mailIndex = Convert.ToInt32(dataGridViewMail["Index", e.RowIndex].Value);
            this.helper_.statusInfo_pro = Tip.fetching;
            enabledWorkArea(false);
            this.Refresh();
            Thread fetchMailThread = new Thread(() =>
            {

                string mail = pop3sp_.fetchMail(mailIndex);

                this.Invoke((Action)(() =>
                {
                    this.helper_.statusInfo_pro = Tip.fetched;
                    if (mail == null)
                    {
                        if (pop3sp_.exception_pro != null)
                        {
                            this.helper_.statusInfo_pro = Tip.noMailContent + pop3sp_.exception_pro.Message;
                        }
                        else
                        {
                            this.helper_.statusInfo_pro = Tip.noMailContent;
                        }
                        return;
                    }
                    FormMail formMail = new FormMail();
                    formMail.Icon = this.Icon;
                    formMail.Width = this.Width;
                    formMail.Height = this.Height;
                    formMail.mail_pro = mail;
                    formMail.ShowDialog();
                    enabledWorkArea(true);
                }));


            });
            fetchMailThread.IsBackground = true;
            fetchMailThread.Start();
        }

        private void enabledWorkArea(bool isEnabled)
        {
            this.groupBoxConnect.Enabled = isEnabled;
            this.groupBoxInfo.Enabled = isEnabled;
        }

        private void buttonPrevious_Click(object sender, EventArgs e)
        {
            fetchMailPage(false);
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            fetchMailPage(true);
        }

        private void buttonSsl_Click(object sender, EventArgs e)
        {

            SslSp sslSp = new SslSp();
            sslSp.connect("pop.gmail.com", 995);
            string receiveStr = sslSp.receive();
            MessageBox.Show(receiveStr);

            sslSp.send("user mysuer\r\n");
            receiveStr = sslSp.receive();
            MessageBox.Show(receiveStr);

            sslSp.send("pass mypassword\r\n");
            receiveStr = sslSp.receive();
            MessageBox.Show(receiveStr);

            int fetchCount = 10;
            sslSp.send("top 1 " + fetchCount.ToString() + "\r\n");
            receiveStr = "";
            int lineCount = 0;
            bool isBeginCount = false;
            Regex endRegex = new Regex(@".*\r\n.\r\n");
            while (true)
            {
                string receiveStrTemp = sslSp.receive();
                string[] lines = receiveStrTemp.Split(new char[] { '\r', '\n' }, StringSplitOptions.None);

                for (int index = 0; index < lines.Length; index++)
                {
                    if (lines[index] == "")
                    {
                        isBeginCount = true;
                    }
                    if (isBeginCount)
                    {
                        lineCount++;
                    }
                }
                receiveStr += receiveStrTemp;
                if (lineCount >= fetchCount)
                {
                    break;
                }
                if (isBeginCount && receiveStrTemp.LastIndexOf(".") >= 0)
                {
                    break;
                }
            }
            MessageBox.Show(receiveStr);
        }
    }
}
