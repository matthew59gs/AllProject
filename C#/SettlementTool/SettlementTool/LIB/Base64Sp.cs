using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SettlementTool
{
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
}
