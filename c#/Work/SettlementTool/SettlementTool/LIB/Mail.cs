using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Globalization;

namespace SettlementTool
{
    public class Mail
    {
        #region receivedate normal Property
        private DateTime maildate_;
        public DateTime maildate_pro
        {
            get
            {
                return maildate_;
            }
            set
            {
                maildate_ = value;
            }
        }
        #endregion

        #region body normal Property
        private string body_ = "Detail";
        public string body_pro
        {
            get
            {
                return body_;
            }
            set
            {
                body_ = value;
            }
        }
        #endregion

        #region from normal Property
        private string from_ = "";
        public string from_pro
        {
            get
            {
                return from_;
            }
            set
            {
                from_ = value;
            }
        }
        #endregion

        #region index normal Property
        private int index_ = 0;
        public int index_pro
        {
            get
            {
                return index_;
            }
            set
            {
                index_ = value;
            }
        }
        #endregion

        #region id normal Property
        private string id_ = "";
        public string id_pro
        {
            get
            {
                return id_;
            }
            set
            {
                id_ = value;
            }
        }
        #endregion

        #region subject normal Property
        private string subject_ = "";
        public string subject_pro
        {
            get
            {
                return subject_;
            }
            set
            {
                subject_ = value;
            }
        }
        #endregion

        #region summary normal Property
        private string summary_ = "";
        public string summary_pro
        {
            get
            {
                return summary_;
            }
            set
            {
                summary_ = value;
            }
        }
        #endregion

        #region to normal Property
        private List<string> to_ = new List<string>();
        public List<string> to_pro
        {
            get
            {
                return to_;
            }
            set
            {
                to_ = value;
            }
        }
        #endregion

        public sealed class FLAG
        {
            public const string DATE = "Date:";
            public const string FROM = "From:";
            public const string TO = "To:";
            public const string SUBJECT = "Subject:";
            public const string SUBJECT_ENCODE_BEGIN = " =?";
            public const string SUBJECT_ENCODE_END = "?B?";//?Q?
            public const string SUBJECT_END = "?=";
        }

        #region fetchDate Function
        /// <summary>
        /// 将日期文本转换为DateTime对象
        /// </summary>
        /// <param name="dateStr">标准格式：Mon, 23 May 2016 16:31:38 +0800 (CST)</param>
        /// <returns></returns>
        public static DateTime fetchDate(string dateStr)
        {
            dateStr += ' ';
            Regex dateRegex = new Regex(@"Date: ([A-Za-z]*,?\s?[0-9]+\s[A-Za-z]+\s[0-9]+\s[0-9]+:[0-9]+:[0-9]+\s\+?-?[0-9]+)\s\(?[A-Za-z]*\)?");
            Match match = dateRegex.Match(dateStr);
            string dateinfo = match.Groups[1].Value.Trim();

            string dateformatWeekday = "ddd, d MMM yyyy HH:mm:ss zz00";
            string dateformat = "d MMM yyyy HH:mm:ss zz00";
            DateTime target;
            if (dateinfo.IndexOf(',') >= 0)
                target = DateTime.ParseExact(dateinfo, dateformatWeekday, CultureInfo.InvariantCulture);
            else
                target = DateTime.ParseExact(dateinfo, dateformat, CultureInfo.InvariantCulture);
            return target;
        }
        #endregion

        #region fetchFrom Function
        public static string fetchFrom(string fromStr)
        {
            Regex fromRegex = new Regex(@"From:");
            Regex encodingInfoRegex = new Regex(@"=?.*?=");
            string fromInfo = fetchNormalStr(fromStr);
            fromStr = encodingInfoRegex.Replace(fromStr, "").Replace(@"""", "").Trim();
            string fromAddress = fromRegex.Replace(fromStr, "").Trim();
            string from = fromInfo + fromAddress;
            return from;
        }
        #endregion

        #region fetchTo Function
        public static string fetchTo(string toStr)
        {
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
            return to;
        }
        #endregion

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
        /// 获取Subject字段
        /// </summary>
        /// <param name="sourceStr">待分析的字符串</param>
        /// <returns></returns>
        public static string fetchSubject(string sourceStr)
        {
            string subject = "";
            const char SplitChar = ':';
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
            return subject;
        }

        /// <summary>
        /// Fetch normal string.
        /// </summary>
        /// <param name="sourceStr">Contain base64 string.Base64 string format is ?.?....?= and ?.? is ?B?/?Q? or other.</param>
        /// <param name="encoding">编码方式，如果不传入，从sourceStr中获取</param>
        /// <returns></returns>
        public static string fetchNormalStr(string sourceStr, Encoding encoding = null)
        {
            if (encoding == null)
                encoding = fetchEncode(sourceStr);
            Regex subjectRegex = new Regex(@"\?.\?.*\?=");
            string subjectBase64 = subjectRegex.Match(sourceStr).Value;
            subjectBase64 = (new Regex(@"\?.\?")).Replace(subjectBase64, "");//replace head.
            subjectBase64 = (new Regex(@"\?=")).Replace(subjectBase64, "");//replace tail.  
            string subject = Base64Sp.toNormalStr(subjectBase64, encoding);
            return subject;
        }

    }
}
