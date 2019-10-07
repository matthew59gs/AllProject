using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.IO;
using System.Net.Security;
using System.Threading;

namespace SettlementTool
{
    /// <summary>
    /// pop3邮件接收处理，必须使用SSL
    /// </summary>
    public class Pop3
    {
        private sealed class POP3_CMD
        {
            public const string CHECK_IS_CONNECT = "noop";//pop.qq.com can check before login.But pop.163.com check after login,or no receive error.
            public const string DELETE = "dele";
            public const string FETCH_MAIL = "retr";
            public const string FETCH_SOME_LINES = "top";
            public const string GET_MAIL_COUNT_VOLUME = "stat ";//Important:tail has a space.            
            public const string GET_ID = "uidl";
            public const string LOGIN_USER = "user";
            public const string LOGIN_PASSWORD = "pass";
            public const string LIST = "list";
            public const string QUIT = "quit";
        }

        private sealed class POP3_RESPONSE_CODE
        {
            public const string OK = "+OK";
            public const string MAIL_END_FLAG = "\r\n.\r\n";
        }

        private class Tip
        {
            public static string mailIndexIllegal = "Mail index is illegal.";
            public static string notConnect = "Not connect or lose host!";
        }

        #region 构造函数
        public Pop3()
        {

        }

        public Pop3(string host)
        {
            sHost = host;
        }

        public Pop3(string host, int port)
        {
            sHost = host;
            iPort = port;
        }
        #endregion

        #region 属性
        private string sHost = "";
        /// <summary>
        /// 主机名或IP
        /// </summary>
        /// <remarks>主机名或IP</remarks>
        public string HostName
        {
            get { return sHost; }
            set { sHost = value; }
        }

        private int iPort = 0;
        /// <summary>
        /// 主机端口
        /// </summary>
        /// <remarks>主机端口</remarks>
        public int Port
        {
            get { return iPort; }
            set { iPort = value; }
        }

        private Encoding encoding_ = Encoding.ASCII;
        /// <summary>
        /// 编码方式，默认ASCII
        /// </summary>
        public Encoding encode
        {
            get { return encoding_; }
            set { encoding_ = value; }
        }

        private Ssl ssl_ = null;
        /// <summary>
        /// 是否已经连接上，默认false
        /// </summary>
        public bool IsConnect
        {
            get { return isConnect(); }
        }

        #endregion

        #region Pop3命令
        /// <summary>
        /// 发送请求
        /// </summary>
        /// <param name="sendstr">发送的命令</param>
        private void send(string sendstr)
        {
            if (ssl_ == null || !ssl_.isConnected)
                new Exception(Tip.notConnect);
            ssl_.send(sendstr + " \r\n");
        }

        /// <summary>
        /// 收取返回的数据，可能返回多行
        /// </summary>
        /// <param name="sendstr">发送的请求，用来判断是否返回多行数据</param>
        /// <returns></returns>
        /// <remarks>在Pop3命令中，LIST、RETR和UIDL命令的结果要返回多行，以点号（.）结尾</remarks>
        private string receive()
        {
            Thread.Sleep(300);
            //if ((sendstr.IndexOf(POP3_CMD.LIST) >= 0) || (sendstr.IndexOf(POP3_CMD.GET_ID) >= 0) || (sendstr.IndexOf(POP3_CMD.FETCH_MAIL) >= 0))
            //{
            //    string sLine = ssl_.receive(), sMultiLine = "";
            //    while (sLine != ".")
            //    {
            //        sMultiLine += sLine + "\r\n";
            //        sLine = ssl_.receive();
            //    }
            //    return sMultiLine;
            //}
            //else
                return ssl_.receive();
        }

        /// <summary>
        /// 当前连接状态
        /// </summary>
        /// <returns>True连接上，False未连接</returns>
        private bool isConnect()
        {
            if (ssl_ == null)
                return false;
            FormMain.log.Debug("send:" + POP3_CMD.CHECK_IS_CONNECT);
            send(POP3_CMD.CHECK_IS_CONNECT);
            string sReceive = receive();
            FormMain.log.Debug("receive[" + POP3_CMD.CHECK_IS_CONNECT + "]" + sReceive);
            if (sReceive.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                return false;
            return true;
        }

        /// <summary>
        /// 与邮件服务器建立连接
        /// </summary>
        /// <returns>
        /// bool
        /// 连接结果：（true成功，false失败）
        /// </returns>
        public bool Connect()
        {
            if (sHost == null)
            {
                throw new Exception("请提供邮件服务器主机名或IP！");
            }

            if (iPort == 0)
            {
                throw new Exception("请提供邮件服务器端口信息！");
            }

            ssl_ = new Ssl();
            ssl_.encoding = encoding_;
            ssl_.connect(sHost, iPort);
            if (!ssl_.isConnected)
                return false;

            string sReceive = receive();
            if (sReceive.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                return false;
            return true;
        }

        /// <summary>
        /// 断开连接
        /// </summary>
        public void Disconnect()
        {
            send(POP3_CMD.QUIT);
            FormMain.log.Debug("send:" + POP3_CMD.QUIT);
        }

        /// <summary>
        /// 登录邮箱
        /// </summary>
        /// <param name="user">用户名</param>
        /// <param name="password">密码</param>
        /// <param name="errMessage">登录失败时返回的错误消息</param>
        /// <returns></returns>
        public bool login(string user, string password, ref string errMessage)
        {
            errMessage = "尚未连接上邮件服务器！";
            if (ssl_ == null)
                return false;

            try
            {
                string sReceive = "";
                errMessage = "用户名错误！";
                FormMain.log.Debug("send:" + POP3_CMD.LOGIN_USER + " " + user);
                send(POP3_CMD.LOGIN_USER + " " + user);
                sReceive = receive();
                FormMain.log.Debug("receive[" + POP3_CMD.LOGIN_USER + "]:" + sReceive);
                //System.Diagnostics.Debug.Assert(false, "登录用户名验证结果：" + sReceive);
                if (sReceive.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                    return false;

                errMessage = "用户密码错误！";
                FormMain.log.Debug("send:" + POP3_CMD.LOGIN_PASSWORD + " *");
                send(POP3_CMD.LOGIN_PASSWORD + " " + password);
                sReceive = receive();
                FormMain.log.Debug("receive[" + POP3_CMD.LOGIN_PASSWORD + "]:" + sReceive);
                //System.Diagnostics.Debug.Assert(false, "登录密码验证结果：" + sReceive);
                if (sReceive.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                    return false;

            }
            catch (Exception ex)
            {
                errMessage = "服务器连接异常！" + ex.Message;
                return false;
            }



            return true;
        }

        /// <summary>
        /// 返回邮件总数
        /// </summary>
        /// <returns>邮件总数</returns>
        public int fetchMailCount()
        {
            send(POP3_CMD.GET_MAIL_COUNT_VOLUME);
            string receiveStr = receive();
            if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                return -1;
            return Convert.ToInt32(receiveStr.Split(' ')[1]);
        }

        /// <summary>
        /// 返回用于该指定邮件的唯一标识
        /// </summary>
        /// <param name="mailIndex">邮件序号</param>
        /// <returns>邮件唯一标识</returns>
        public string fetchId(int mailIndex)
        {
            FormMain.log.Debug("send:" + POP3_CMD.GET_ID + " " + mailIndex.ToString());
            send(POP3_CMD.GET_ID + " " + mailIndex.ToString());
            //string receiveStr = receive(POP3_CMD.GET_ID);
            string receiveStr = receive();
            FormMain.log.Debug("receive[" + POP3_CMD.GET_ID + "]:" + receiveStr);
            if (receiveStr.Split(' ').Length >= 2)
            {
                return receiveStr.Split(' ')[2].Replace("\r\n", "");
            }
            return "";
        }

        /// <summary>
        /// 获取特定邮件
        /// </summary>
        /// <param name="mailIndex">邮件编号</param>
        /// <returns></returns>
        public string fetchMail(int mailIndex)
        {
            if (!isConnect())
                return "";

            send(POP3_CMD.FETCH_MAIL + " " + mailIndex.ToString());
            return receiveAll(-1, POP3_CMD.FETCH_MAIL);
        }

        /// <summary>
        /// 获取特定批次的邮件摘要
        /// </summary>
        /// <param name="beginMailIndex">特定批次邮件的起始序号</param>
        /// <param name="endMailIndex">特定批次邮件的结束序号</param>
        /// <returns>Mail对象的List</returns>
        public List<Mail> fetchMailList(int beginMailIndex, int endMailIndex)
        {
            if (!isConnect())
            {
                return null;
            }

            if (beginMailIndex <= 0 || endMailIndex <= 0)
                return null;

            List<Mail> mailList = new List<Mail>();
            for (int mailIndex = beginMailIndex; mailIndex <= endMailIndex; mailIndex++)
            {
                try
                {
                    FormMain.log.Info("获取Index=" + mailIndex.ToString() + "的邮件摘要");
                    Mail mail = fetchMailSummary(mailIndex, 5);
                    if (mail != null)
                    {
                        mail.index_pro = mailIndex;
                        FormMain.log.Info("获取Index=" + mailIndex.ToString() + "的邮件ID");
                        mail.id_pro = fetchId(mailIndex);
                    }
                    mailList.Add(mail);
                }
                catch (Exception ex)
                {
                    throw new Exception("邮件索引编号：" + mailIndex.ToString() + "\n" + ex.Message);
                }
            }

            return mailList;
        }

        /// <summary>
        /// 将返回的多条消息组成长文本返回
        /// </summary>
        /// <param name="fetchCount">待收取的消息数量</param>
        /// <returns>多条消息组成的长文本，各个消息用\r\n隔开</returns>
        private string receiveAll(int fetchCount, string strSendCmd = "")
        {
            string receiveStr = "";
            //int lineCount = -1; // 这里原来是0，但是有BUG，会导致实际少receive了一行
            //bool isBeginCount = false;
            while (true)
            {
                string receiveStrTemp = receive();
                FormMain.log.Debug("receive[" + strSendCmd + "]:" + receiveStrTemp);
                //string[] lines = receiveStrTemp.Split(new char[] { '\r', '\n' }, StringSplitOptions.None);
                //for (int index = 0; index < lines.Length; index++)
                //{
                //    if (lines[index] == "")
                //    {
                //        isBeginCount = true;
                //    }
                //    if (isBeginCount)
                //    {
                //        lineCount++;
                //    }
                //}
                receiveStr += receiveStrTemp + "\r\n";
                //if (fetchCount > 0 && lineCount >= fetchCount)
                //{
                //    break;
                //}
                //if (isBeginCount && receiveStrTemp.LastIndexOf(".") >= 0)
                if (receiveStrTemp.LastIndexOf(".") == 0)
                {
                    break;
                }
            }
            return receiveStr;
        }

        /// <summary>
        /// 获取特定批次的邮件摘要
        /// </summary>
        /// <param name="mailIndex">特定批次的邮件起始位置</param>
        /// <param name="fetchCount">此批次邮件数量</param>
        /// <returns>mail对象</returns>
        public Mail fetchMailSummary(int mailIndex, int fetchCount)
        {
            FormMain.log.Debug("send:" + POP3_CMD.FETCH_SOME_LINES + " " + mailIndex.ToString() + " " + fetchCount.ToString());
            send(POP3_CMD.FETCH_SOME_LINES + " " + mailIndex.ToString() + " " + fetchCount.ToString());
            string mailSummary = receiveAll(fetchCount, POP3_CMD.FETCH_SOME_LINES);
            FormMain.log.Info("获取到Index=" + mailIndex.ToString() + "的摘要：\n" + mailSummary);
            Mail mail = analySummary(mailSummary);
            return mail;
        }

        /// <summary>
        /// 将文本摘要转换为mail对象
        /// </summary>
        /// <param name="mailSummary">邮件的文本摘要</param>
        /// <returns>mail对象</returns>
        public Mail analySummary(string mailSummary)//Need fix if server is gmail.
        {
            string[] lines = mailSummary.Split(new string[] { "\n" }, StringSplitOptions.RemoveEmptyEntries);
            Mail mail = new Mail();
            try
            {
                foreach (string line in lines)
                {
                    if (line.IndexOf(Mail.FLAG.FROM) == 0)
                    {
                        FormMain.log.Info("分析邮件的FROM字段：" + line);
                        mail.from_pro = Mail.fetchFrom(line);
                        mail.summary_pro += Mail.FLAG.FROM + mail.from_pro + "\r\n";
                    }
                    else if (line.IndexOf(Mail.FLAG.TO) == 0)
                    {
                        FormMain.log.Info("分析邮件的TO字段：" + line);
                        string to = Mail.fetchTo(line);
                        mail.to_pro.Add(to);
                        mail.summary_pro += Mail.FLAG.TO + to + "\r\n";
                    }
                    else if (line.IndexOf(Mail.FLAG.SUBJECT) == 0)
                    {
                        FormMain.log.Info("分析邮件的SUBJECT字段：" + line);
                        mail.subject_pro = Mail.fetchSubject(line);
                        mail.summary_pro += Mail.FLAG.SUBJECT + mail.subject_pro + "\r\n";
                    }
                    else if (line.IndexOf(Mail.FLAG.DATE) == 0)
                    {
                        FormMain.log.Info("分析邮件的DATE字段：" + line);
                        mail.maildate_pro = Mail.fetchDate(line);
                        mail.summary_pro += Mail.FLAG.DATE + mail.maildate_pro.ToShortDateString() + "\r\n";
                    }
                }
            }
            catch (Exception ex)
            {
                throw new Exception("邮件原文：" + mailSummary + "\n" + ex.Message);
            }
            FormMain.log.Info("邮件信息：" + mail.summary_pro);
            return mail;
        }
        #endregion
    }
}
