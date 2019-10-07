using System;
using System.IO;
using System.Net;
using System.Text.RegularExpressions;
using System.Management;

namespace DunhePublic
{
    public class GetSystemInfo
    {
        /// <summary>  
        /// 获取客户端内网IPv4地址  
        /// </summary>  
        /// <returns>客户端内网IPv4地址</returns>  
        public static string GetClientLocalIPv4Address()
        {
            string strLocalIP = string.Empty;
            try
            {
                IPHostEntry ipHost = Dns.Resolve(Dns.GetHostName());
                IPAddress ipAddress = ipHost.AddressList[0];
                strLocalIP = ipAddress.ToString();
                return strLocalIP;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取本机公网IP地址  
        /// </summary>  
        /// <returns>本机公网IP地址</returns>  
        public static string GetClientInternetIPAddress()
        {
            try
            {
                WebClient client = new WebClient();
                client.Encoding = System.Text.Encoding.Default;
                string response = client.DownloadString("http://icanhazip.com/");
                return response.Trim();
            }
            catch (Exception)
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取本机MAC地址  
        /// </summary>  
        /// <returns>本机MAC地址</returns>  
        public static string GetMacAddress()
        {
            try
            {
                string strMac = string.Empty;
                ManagementClass mc = new ManagementClass("Win32_NetworkAdapterConfiguration");
                ManagementObjectCollection moc = mc.GetInstances();
                foreach (ManagementObject mo in moc)
                {
                    if ((bool)mo["IPEnabled"] == true)
                    {
                        strMac = mo["MacAddress"].ToString();
                    }
                }
                moc = null;
                mc = null;
                return strMac;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取硬盘序号  
        /// </summary>  
        /// <returns>硬盘序号</returns>  
        public static string GetDiskID()
        {
            try
            {
                string strDiskID = string.Empty;
                ManagementClass mc = new ManagementClass("Win32_DiskDrive");
                ManagementObjectCollection moc = mc.GetInstances();
                foreach (ManagementObject mo in moc)
                {
                    strDiskID = mo.Properties["Model"].Value.ToString();
                }
                moc = null;
                mc = null;
                return strDiskID;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取CpuID  
        /// </summary>  
        /// <returns>CpuID</returns>  
        public static string GetCpuID()
        {
            try
            {
                string strCpuID = string.Empty;
                ManagementClass mc = new ManagementClass("Win32_Processor");
                ManagementObjectCollection moc = mc.GetInstances();
                foreach (ManagementObject mo in moc)
                {
                    strCpuID = mo.Properties["ProcessorId"].Value.ToString();
                }
                moc = null;
                mc = null;
                return strCpuID;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取操作系统类型  
        /// </summary>  
        /// <returns>操作系统类型</returns>  
        public static string GetSystemType()
        {
            try
            {
                string strSystemType = string.Empty;
                ManagementClass mc = new ManagementClass("Win32_ComputerSystem");
                ManagementObjectCollection moc = mc.GetInstances();
                foreach (ManagementObject mo in moc)
                {
                    strSystemType = mo["SystemType"].ToString();
                }
                moc = null;
                mc = null;
                return strSystemType;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取操作系统名称  
        /// </summary>  
        /// <returns>操作系统名称</returns>  
        public static string GetSystemName()
        {
            try
            {
                string strSystemName = string.Empty;
                ManagementObjectSearcher mos = new ManagementObjectSearcher("root\\CIMV2", "SELECT PartComponent FROM Win32_SystemOperatingSystem");
                foreach (ManagementObject mo in mos.Get())
                {
                    strSystemName = mo["PartComponent"].ToString();
                }
                mos = new ManagementObjectSearcher("root\\CIMV2", "SELECT Caption FROM Win32_OperatingSystem");
                foreach (ManagementObject mo in mos.Get())
                {
                    strSystemName = mo["Caption"].ToString();
                }
                return strSystemName;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取物理内存信息  
        /// </summary>  
        /// <returns>物理内存信息</returns>  
        public static string GetTotalPhysicalMemory()
        {
            try
            {
                string strTotalPhysicalMemory = string.Empty;
                ManagementClass mc = new ManagementClass("Win32_ComputerSystem");
                ManagementObjectCollection moc = mc.GetInstances();
                foreach (ManagementObject mo in moc)
                {
                    strTotalPhysicalMemory = mo["TotalPhysicalMemory"].ToString();
                }
                moc = null;
                mc = null;
                return strTotalPhysicalMemory;
            }
            catch
            {
                return "unknown";
            }
        }

        /// <summary>  
        /// 获取主板id  
        /// </summary>  
        /// <returns></returns>  
        public static string GetMotherBoardID()
        {
            try
            {
                ManagementClass mc = new ManagementClass("Win32_BaseBoard");
                ManagementObjectCollection moc = mc.GetInstances();
                string strID = null;
                foreach (ManagementObject mo in moc)
                {
                    strID = mo.Properties["SerialNumber"].Value.ToString();
                    break;
                }
                return strID;
            }
            catch
            {
                return "unknown";
            }
        }
    }
}
