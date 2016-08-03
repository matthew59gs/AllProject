using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Security;
using System.Net.Sockets;
using System.IO;

namespace SettlementTool
{
    public class Ssl
    {
        #region Property
        private Encoding encoding_ = Encoding.ASCII;
        /// <summary>
        /// 编码方式，默认ASCII
        /// </summary>
        public Encoding encoding
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

        private bool isConnected_ = false;
        /// <summary>
        /// 是否已经连接上
        /// </summary>
        public bool isConnected
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
        /// <summary>
        /// SSL连接
        /// </summary>
        /// <param name="host">主机地址或IP</param>
        /// <param name="port">端口</param>
        public void connect(string host, int port)
        {
            isConnected_ = false;
            TcpClient popServer = new TcpClient(host, port);
            pop3Stream_ = new SslStream(popServer.GetStream(), false);
            pop3Stream_.AuthenticateAsClient(host);
            isConnected_ = true;
            pop3StreamReader_ = new StreamReader(pop3Stream_, encoding_);
        }

        /// <summary>
        /// 发送请求
        /// </summary>
        /// <param name="sendStr">请求数据</param>
        public void send(string sendStr)
        {
              pop3Stream_.Write(encoding_.GetBytes(sendStr));
        }

        /// <summary>
        /// 读一行返回数据
        /// </summary>
        /// <returns>返回一行数据</returns>
        public string receive()
        {
            return pop3StreamReader_.ReadLine();
        }
        #endregion
    }
}
