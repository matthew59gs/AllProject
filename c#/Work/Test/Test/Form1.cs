using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Text.RegularExpressions;
using System.Globalization;

namespace Test
{
    public partial class Form1 : Form
    {
        private delegate bool IncreaseHandle(int iValue);   //代理创建
        private IncreaseHandle myIncrease = null;           //声明代理，用于后面的实例化代理
        private const int iMaX = 32;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Test3();
        }

        /// <summary>
        /// 日期字段的拆分
        /// </summary>
        private void Test1()
        {
            string test1 = "Date: 6 Jun 2016 04:50:02 -0400 ";
            string test2 = "Date: Tue, 24 May 2016 16:44:55 +0800 (CST)";
            string test3 = "Date: Tue, 24 May 2016 16:32:58 +0800 ";
            //Regex dateRegex = new Regex(@"Date:(.+)\(?(\S+)\)?");
            //Regex dateRegex = new Regex(@"Date: ([A-Za-z]*,?\s?[0-9]+\s[A-Za-z]+\s[0-9]+:[0-9]+:[0-9]+\s\+|\-[0-9]+)\s\(?([A-Z]+)\)?");
            Regex dateRegex = new Regex(@"Date: ([A-Za-z]*,?\s?[0-9]+\s[A-Za-z]+\s[0-9]+\s[0-9]+:[0-9]+:[0-9]+\s\+?-?[0-9]+)\s\(?[A-Za-z]*\)?");
            Match match = dateRegex.Match(test1);
            string dateinfo = match.Groups[1].Value.Trim();

            string dateformatWeekday = "ddd, d MMM yyyy HH:mm:ss zz00";
            string dateformat = "d MMM yyyy HH:mm:ss zz00";
            DateTime target;
            if (dateinfo.IndexOf(',') >= 0)
                target = DateTime.ParseExact(dateinfo, dateformatWeekday, CultureInfo.InvariantCulture);
            else
                target = DateTime.ParseExact(dateinfo, dateformat, CultureInfo.InvariantCulture);
            target = TimeZoneInfo.ConvertTimeBySystemTimeZoneId(target, TimeZoneInfo.Local.Id);
            MessageBox.Show(target.ToLongTimeString());
        }

        /// <summary>
        /// To字段的拆分
        /// </summary>
        private void Test2()
        {
            string toStr = "To: \"=?utf-8?B?5rKI5pet5qyj?=\" <shenxx@dunhefund.com>, \"=?utf-8?B?6auY5bWp?=\" <gaos@dunhefund.com>";
            Regex toRegex = new Regex(@"To:");
            Regex quotesRegex = new Regex("\"");
            Regex encodingInfoRegex = new Regex(@"=?.*?=");
            string toTmpStr = quotesRegex.Replace(toStr, "");
            toTmpStr = toRegex.Replace(toTmpStr, "");
            string[] toStrList = toTmpStr.Split(',');
            string to = "";
            for (int i = 0; i < toStrList.Count(); ++i)
            {
                string toSepStr = toStrList[i];
                string toInfo = fetchNormalStr(toSepStr);
                string toAddress = encodingInfoRegex.Replace(toSepStr, "").Replace(@"""", "").Trim();
                to += toInfo + toAddress;
            }
            MessageBox.Show(to);
        }

        /// <summary>
        /// Subject字段拆分
        /// </summary>
        private void Test3()
        {
            string subject = "";
            const char SplitChar = ':';
            //string sourceStr = "Subject: FW: =?UTF-8?B?562U5aSN?=: =?UTF-8?B?IOWbveWvjOacn+i0pw==?=";
            string sourceStr = "Subject: =?gb2312?B?0MXPos+1zbPKudPDx+m/9qOssO/O0sPHzO7Su8/C?=";
            Regex SubjectRegex = new Regex(@"Subject:");
            Regex DivisionRegex = new Regex(@":");
            string SubjectTmpStr = SubjectRegex.Replace(sourceStr, "");
            string[] subjectList = SubjectTmpStr.Split(SplitChar);

            for (int i = 0; i < subjectList.Count(); ++i)
            {
                string strTmp = subjectList[i];
                if (strTmp.IndexOf("=?") < 0)
                    subject += strTmp;
                else
                    subject += fetchNormalStr(strTmp);
                subject += SplitChar;
            }
            subject = subject.Substring(0, subject.Length - 1);
            MessageBox.Show(subject);
        }


        /// <summary>
        /// Fetch encoder from source string.
        /// </summary>
        /// <param name="sourceStr">Format is =?...?.? and ?.? is ?B?/?Q? or other.</param>
        /// <returns></returns>
        public static Encoding fetchEncode(string sourceStr)
        {
            if (!hasEncoderInfo(sourceStr))
            {
                return Encoding.UTF8;
            }
            Regex encodingNameRegex = new Regex(@"=\?.*\?.\?");
            string encodingName = encodingNameRegex.Match(sourceStr).Value;
            encodingName = (new Regex(@"=\?")).Replace(encodingName, "");//replace head.
            encodingName = (new Regex(@"\?.\?")).Replace(encodingName, "");//replace tail.            
            encodingName = encodingName.ToUpper();      // 编码方式
            return Encoding.GetEncoding(encodingName);
        }

        #region hasEncoderInfo Function
        public static bool hasEncoderInfo(string sourceStr)
        {
            Regex encodingNameRegex = new Regex(@"=\?.*\?.\?");
            return encodingNameRegex.IsMatch(sourceStr);
        }
        #endregion

        /// <summary>
        /// Fetch normal string.
        /// </summary>
        /// <param name="sourceStr">Contain encoder informaion and base64 string.
        /// Encoder information format is =?...?.? and ?.? is ?B?/?Q? or other.
        /// Base64 string format is ?.?....?= and ?.? is ?B?/?Q? or other.
        /// </param>
        /// <returns></returns>
        public static string fetchNormalStr(string sourceStr)
        {
            Encoding encoding = fetchEncode(sourceStr);
            Regex subjectRegex = new Regex(@"\?.\?.*\?=");
            string subjectBase64 = subjectRegex.Match(sourceStr).Value;
            subjectBase64 = (new Regex(@"\?.\?")).Replace(subjectBase64, "");//replace head.
            subjectBase64 = (new Regex(@"\?=")).Replace(subjectBase64, "");//replace tail.  
            // subjectBase64 = subjectBase64.Replace("=", "").Trim();
            //subjectBase64 = subjectBase64.PadRight((subjectBase64.Length + 2) / 3 * 3, '=');
            string subject = Base64Sp.toNormalStr(subjectBase64, encoding);
            return subject;
        }

        public class Base64Sp
        {
            /// <summary>
            /// To base 64 string.
            /// </summary>
            /// <param name="sourceStr">sourceStr</param>
            /// <param name="encoding">Encoding is null,use default encoding.</param>
            /// <returns></returns>
            public static string tobase64Str(string sourceStr, Encoding encoding = null)
            {
                if (encoding == null)
                {
                    encoding = Encoding.Default;
                }
                byte[] bytes = encoding.GetBytes(sourceStr);
                string base64Str = Convert.ToBase64String(bytes);
                return base64Str;
            }

            /// <summary>
            /// To base 64 string.
            /// </summary>
            /// <param name="sourceStr">sourceStr</param>
            /// <param name="encoding">Encoding is null,use default encoding.</param>
            /// <returns></returns>
            public static byte[] tobase64Bytes(string sourceStr, Encoding encoding = null)
            {
                if (encoding == null)
                {
                    encoding = Encoding.Default;
                }
                return encoding.GetBytes(sourceStr);
            }

            /// <summary>
            /// Base64 string to normal string.
            /// </summary>
            /// <param name="base64Str">sourceStr</param>
            /// <param name="encoding">Encoding is null,use default encoding.</param>
            /// <returns></returns>
            public static string toNormalStr(string base64Str, Encoding encoding = null)
            {
                try
                {
                    if (string.IsNullOrEmpty(base64Str))
                    {
                        return "";
                    }

                    if (encoding == null)
                    {
                        encoding = Encoding.Default;
                    }
                    byte[] bytes = Convert.FromBase64String(base64Str);
                    return encoding.GetString(bytes);
                }
                catch (System.Exception ex)
                {
                    return ex.Message;
                }
            }
        }

        private void buttonPB_Click(object sender, EventArgs e)
        {
            backgroundWorker1.RunWorkerAsync();
            backgroundworker_PB form = new backgroundworker_PB(backgroundWorker1);
            form.ShowDialog();
            form.Close();
        }

        private void backgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            BackgroundWorker worker = sender as BackgroundWorker;
            for (int i = 0; i < 100; i++)
            {
                Thread.Sleep(100);
                worker.ReportProgress(i);
                if (worker.CancellationPending)  // 如果用户取消则跳出处理数据代码 
                {
                    e.Cancel = true;
                    MessageBox.Show("User Canceled!");
                    break;
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Thread thdSub = new Thread(new ThreadStart(ThreadFun));
            thdSub.Start();
        }

        private void ThreadFun()
        {
            MethodInvoker mi = new MethodInvoker(ShowProcessBar);
            this.BeginInvoke(mi);
            Thread.Sleep(100);
            object objReturn = null;
            for (int i = 0; i < iMaX; i++)
            {
                objReturn = this.Invoke(this.myIncrease, new object[] { 1 });
                Thread.Sleep(50);
            }
        }

        private void ShowProcessBar()
        {
            thread_PB myProcessBar = new thread_PB(iMaX);
            myIncrease = new IncreaseHandle(myProcessBar.increase);
            myProcessBar.ShowDialog();
        }
    }
}
