using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace UtilSp.ClassLib
{
    public class MailSp
    {
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
            public const string FROM = "From:";
            public const string TO = "To:";
            public const string SUBJECT = "Subject:";
            public const string SUBJECT_ENCODE_BEGIN = " =?";
            public const string SUBJECT_ENCODE_END = "?B?";//?Q?
            public const string SUBJECT_END = "?=";
        }

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
            Regex encodingInfoRegex = new Regex(@"=?.*?=");
            string toInfo = fetchNormalStr(toStr);
            toStr = encodingInfoRegex.Replace(toStr, "").Replace(@"""", "").Trim();
            string toAddress = toRegex.Replace(toStr, "").Trim();
            string to = toInfo + toAddress;
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

        /// <summary>
        /// Fetch normal string.
        /// </summary>
        /// <param name="sourceStr">Contain base64 string.Base64 string format is ?.?....?= and ?.? is ?B?/?Q? or other.</param>
        /// <param name="encoding"></param>
        /// <returns></returns>
        public static string fetchNormalStr(string sourceStr, Encoding encoding)
        {
            Regex subjectRegex = new Regex(@"\?.\?.*\?=");
            string subjectBase64 = subjectRegex.Match(sourceStr).Value;
            subjectBase64 = (new Regex(@"\?.\?")).Replace(subjectBase64, "");//replace head.
            subjectBase64 = (new Regex(@"\?=")).Replace(subjectBase64, "");//replace tail.  
            string subject = Base64Sp.toNormalStr(subjectBase64, encoding);
            return subject;
        }

    }
}
