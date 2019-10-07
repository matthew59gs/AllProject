using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Threading;
using System.Text.RegularExpressions;

namespace UtilSp.ClassLib
{
    public class Pop3Sp
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

        #region member

        #region encoding_send normal Property
        private Encoding encoding_send_ = Encoding.UTF8;
        public Encoding encoding_send_pro
        {
            get
            {
                return encoding_send_;
            }
            set
            {
                encoding_send_ = value;
            }
        }
        #endregion

        #region encoding_receive normal Property
        private Encoding encoding_receive_ = Encoding.UTF8;
        public Encoding encoding_receive_pro
        {
            get
            {
                return encoding_receive_;
            }
            set
            {
                encoding_receive_ = value;
            }
        }
        #endregion

        #region exception normal Property
        private Exception exception_ = null;
        public Exception exception_pro
        {
            get
            {
                return exception_;
            }
            set
            {
                exception_ = value;
            }
        }
        #endregion

        #region isSsl normal Property
        private bool isSsl_ = false;
        public bool isSsl_pro
        {
            get
            {
                return isSsl_;
            }
            set
            {
                isSsl_ = value;
            }
        }
        #endregion

        #region socket normal Property
        private Socket socket_;
        public Socket socket_pro
        {
            get
            {
                return socket_;
            }
            private set
            {
                socket_ = value;
            }
        }
        #endregion

        #region ssl normal Property
        private SslSp ssl_ = null;
        public SslSp ssl_pro
        {
            get
            {
                return ssl_;
            }
            set
            {
                ssl_ = value;
            }
        }
        #endregion

        #region receiveLen_max normal Property
        private int receiveLen_max_ = 0xFFFF;
        public int receiveLen_max_pro
        {
            get
            {
                return receiveLen_max_;
            }
            set
            {
                receiveLen_max_ = value;
            }
        }
        #endregion

        #endregion

        #region connect Function
        public bool connect(string host, int port)
        {
            try
            {
                exception_pro = null;
                if (isSsl_pro)
                {
                    ssl_pro = new SslSp();
                    ssl_pro.connect(host, port);
                }
                else
                {
                    socket_ = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                    socket_.Connect(host, port);
                }
                if (isSsl_pro && !ssl_pro.isConnected_pro)
                {
                    if (ssl_pro.exception_pro != null)
                    {
                        exception_pro = new Exception(Tip.notConnect + ssl_pro.exception_pro.Message);
                    }
                    else
                    {
                        exception_pro = new Exception(Tip.notConnect);
                    }
                    return false;
                }
                if (!isSsl_pro && !socket_.Connected)
                {
                    exception_pro = new Exception(Tip.notConnect);
                    return false;
                }

                string receiveStr = receive();
                if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                {
                    return false;
                }
                return isSsl_pro ? ssl_pro.isConnected_pro : socket_.Connected;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return false;
            }
        }

        public bool connect(string host, int port, bool isSsl)
        {
            try
            {
                exception_pro = null;
                socket_ = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                socket_.Connect(host, port);
                string receiveStr = receive();
                if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                {
                    return false;
                }
                return socket_.Connected;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return false;
            }
        }
        #endregion

        #region delete Function
        public bool delete(int mailIndex)
        {
            if (!send(POP3_CMD.DELETE + " " + mailIndex.ToString() + "\r\n"))
            {
                return false;
            }
            string receiveStr = receive();
            if (receiveStr.LastIndexOf(POP3_RESPONSE_CODE.OK) == 0)
            {
                return true;
            }
            return false;
        }
        #endregion

        #region disconnect Function
        public bool disconnect()
        {
            try
            {
                exception_pro = null;
                if (socket_pro == null)
                {
                    return true;
                }
                if (!isConnect())
                {
                    return true;
                }
                if (!send(POP3_CMD.QUIT + " \r\n"))
                {
                    return false;
                }
                socket_pro.Close();
                return !socket_pro.Connected;
            }
            catch (System.Exception ex)
            {
                socket_pro = null;
                return false;
            }
        }
        #endregion

        #region fetchId Function
        public string fetchId(int mailIndex)
        {


            if (!send(POP3_CMD.GET_ID + " " + mailIndex.ToString() + "\r\n"))
            {
                return null;
            }
            string receiveStr = receive();
            if (receiveStr.Split(' ').Length >= 2)
            {
                return receiveStr.Split(' ')[2].Replace("\r\n", "");
            }
            return "";




        }
        #endregion

        public int fetchMailCount()
        {
            try
            {
                exception_pro = null;
                if (!send(POP3_CMD.GET_MAIL_COUNT_VOLUME + "\r\n"))
                {
                    return -1;
                }
                string receiveStr = receive();
                if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                {
                    exception_pro = new Exception(receiveStr);
                    return -1;
                }
                int mailCount = Convert.ToInt32(receiveStr.Split(' ')[1]);
                return mailCount;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return -1;
            }
        }

        #region fetchMailList Function
        public List<MailSp> fetchMailList(int beginMailIndex, int endMailIndex)
        {
            try
            {
                exception_pro = null;
                if (!isConnect())
                {
                    return null;
                }

                if (beginMailIndex <= 0 || endMailIndex <= 0)
                {
                    exception_pro = new Exception(Tip.mailIndexIllegal);
                    return null;
                }
                List<MailSp> mailList = new List<MailSp>();
                for (int mailIndex = beginMailIndex; mailIndex <= endMailIndex; mailIndex++)
                {
                    try
                    {
                        MailSp mail = fetchMailSummary(mailIndex, 5);
                        if (mail != null)
                        {
                            mail.index_pro = mailIndex;
                            mail.id_pro = fetchId(mailIndex);
                        }
                        mailList.Add(mail);
                    }
                    catch (System.Exception ex)
                    {
                        Console.WriteLine("fetchMailList exception:" + ex.Message);
                        continue;
                    }
                }

                return mailList;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return null;
            }
        }

        public string fetchMail(int mailIndex)
        {
            if (!isConnect())
            {
                return null;
            }

            if (!send(POP3_CMD.FETCH_MAIL + " " + mailIndex.ToString() + "\r\n"))
            {
                return null;
            }
            string mail = receiveAll(-1);
            //while (true)
            //{
            //    string receiveStr = receive();
            //    mail += receiveStr;
            //    if (receiveStr.LastIndexOf(POP3_RESPONSE_CODE.MAIL_END_FLAG) > 0)
            //    {
            //        break;
            //    }
            //}
            return mail;
        }

        public MailSp fetchMailSummary(int mailIndex, int fetchCount)
        {
            if (!send(POP3_CMD.FETCH_SOME_LINES + " " + mailIndex.ToString() + " " + fetchCount.ToString() + " \r\n"))
            {
                return null;
            }
            string mailSummary = receiveAll(fetchCount);
            MailSp mail = analySummary(mailSummary);
            return mail;
        }

        /// <summary>
        /// Receive all data.
        /// </summary>
        /// <param name="fetchCount">Less than or equal 0:fetch data until end.More than 0:fetch data until end or reach fetchCount.</param>
        /// <returns></returns>
        private string receiveAll(int fetchCount)
        {
            string receiveStr = "";
            int lineCount = 0;
            bool isBeginCount = false;
            while (true)
            {
                string receiveStrTemp = receive();
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
                if (fetchCount > 0 && lineCount >= fetchCount)
                {
                    break;
                }
                if (isBeginCount && receiveStrTemp.LastIndexOf(".") >= 0)
                {
                    break;
                }
            }
            return receiveStr;
        }

        public MailSp analySummary(string mailSummary)//Need fix if server is gmail.
        {
            string[] lines = mailSummary.Split(new string[] { "\n" }, StringSplitOptions.RemoveEmptyEntries);
            MailSp mail = new MailSp();
            foreach (string line in lines)
            {
                if (line.IndexOf(MailSp.FLAG.FROM) == 0)
                {
                    mail.from_pro = MailSp.fetchFrom(line);
                    mail.summary_pro += MailSp.FLAG.FROM + mail.from_pro + "\r\n";
                }
                else if (line.IndexOf(MailSp.FLAG.TO) == 0)
                {
                    string to = MailSp.fetchTo(line);
                    mail.to_pro.Add(to);
                    mail.summary_pro += MailSp.FLAG.TO + to + "\r\n";
                }
                else if (line.IndexOf(MailSp.FLAG.SUBJECT) == 0)
                {
                    mail.subject_pro = MailSp.fetchNormalStr(line);
                    mail.summary_pro += MailSp.FLAG.SUBJECT + mail.subject_pro;
                }
            }
            return mail;
        }


        #endregion

        #region getExceptionStr Function
        public string getExceptionStr()
        {
            return exception_pro == null ? "" : exception_pro.Message;
        }
        #endregion

        #region isConnect Function
        public bool isConnect()
        {
            try
            {
                exception_pro = null;
                if (!send(POP3_CMD.CHECK_IS_CONNECT + " \r\n"))
                {
                    return false;
                }
                string receiveStr = receive();
                if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                {
                    exception_pro = new Exception(Tip.notConnect);
                    return false;
                }
                return true;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return false;
            }
        }
        #endregion

        #region login Function
        public bool login(string userName, string password)
        {
            try
            {
                exception_pro = null;

                #region  user login

                if (!send(POP3_CMD.LOGIN_USER + " " + userName + "\r\n"))
                {
                    return false;
                }
                string receiveStr = receive();
                if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                {
                    exception_pro = new Exception(receiveStr);
                    return false;
                }
                #endregion

                #region password login
                send(POP3_CMD.LOGIN_PASSWORD + " " + password + "\r\n");
                receiveStr = "";
                receiveStr = receive();
                if (receiveStr.IndexOf(POP3_RESPONSE_CODE.OK) != 0)
                {
                    exception_pro = new Exception(receiveStr);
                    return false;
                }
                #endregion

                return true;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return false;
            }
        }
        #endregion

        private string receive()
        {
            string receiveStr = "";
            Thread.Sleep(300);
            if (isSsl_pro)
            {
                receiveStr = ssl_pro.receive();
            }
            else
            {
                byte[] receiveBuffer = new byte[receiveLen_max_pro];
                int receiveLength = socket_pro.Receive(receiveBuffer);
                receiveStr = encoding_receive_pro.GetString(receiveBuffer, 0, receiveLength);
            }
            return receiveStr;
        }

        private bool send(string sendStr)
        {
            if (isSsl_pro)
            {
                if (ssl_pro == null || !ssl_pro.isConnected_pro)
                {
                    exception_pro = ssl_pro.exception_pro == null ? new Exception(Tip.notConnect) : ssl_pro.exception_pro;
                    return false;
                }
                ssl_pro.send(sendStr);
            }
            else
            {
                if (socket_pro == null || !socket_pro.Connected)
                {
                    exception_pro = new Exception(Tip.notConnect);
                    return false;
                }
                byte[] sendBuffer = encoding_send_pro.GetBytes(sendStr);
                socket_pro.Send(sendBuffer);
            }
            return true;
        }

        private class Tip
        {
            public static string mailIndexIllegal = "Mail index is illegal.";
            public static string notConnect = "Not connect or lose host!";
        }
    }
}
