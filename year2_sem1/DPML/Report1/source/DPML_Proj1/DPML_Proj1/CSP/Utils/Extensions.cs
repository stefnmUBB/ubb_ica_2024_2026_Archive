using System.Collections.Generic;

namespace DPML_Proj1.CSP.Utils
{
    public static class Extensions
    {
        public static IEnumerable<(T,T)> EnumeratePairs<T>(this T[] items)
        {
            for(int i=0;i<items.Length;i++)
            {
                for (int j = i + 1; j < items.Length; j++)
                {
                    yield return (items[i], items[j]);
                }
            }
        }
    }
}
