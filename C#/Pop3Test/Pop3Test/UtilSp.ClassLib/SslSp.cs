using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Security;
using System.Net.Sockets;
using System.Text;

namespace UtilSp.ClassLib
{
    public class SslSp
    {
        #region encoding normal Property
        private Encoding encoding_ = Encoding.ASCII;
        public Encoding encoding_pro
        {
            get
            {
                return encoding_;
            }
            set
            {
                encoding_ = value;
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

        #region isConnected normal Property
        private bool isConnected_ = false;
        public bool isConnected_pro
        {
            get
            {
                return isConnected_;
            }
            set
            {
                isConnected_ = value;
            }
        }
        #endregion

        private StreamReader pop3StreamReader_ = null;
        private SslStream pop3Stream_ = null;

        #region connectSsl Function
        public void connect(string host, int port)
        {
            try
            {

                TcpClient popServer = new TcpClient(host, port);

                pop3Stream_ = new SslStream(popServer.GetStream(), false);
                pop3Stream_.AuthenticateAsClient(host);
                isConnected_pro = true;
                pop3StreamReader_ = new StreamReader(pop3Stream_, encoding_pro);
                
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                isConnected_pro = false;
            }
        }

        public bool send(string sendStr)
        {
            try
            {
                exception_pro = null;
                pop3Stream_.Write(encoding_pro.GetBytes(sendStr));
                return true;
            }
            catch (System.Exception ex)
            {
                exception_pro = ex;
                return false;
            }
        }

        /// <summary>
        /// Receive one line data.
        /// </summary>
        /// <returns></returns>
        public string receive()
        {
            string receiveStr = "";
            receiveStr = pop3StreamReader_.ReadLine();
            return receiveStr;
        }
        #endregion
    }
}
