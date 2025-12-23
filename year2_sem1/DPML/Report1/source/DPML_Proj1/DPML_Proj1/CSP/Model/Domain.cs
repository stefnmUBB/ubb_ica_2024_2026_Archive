using System.Collections.Generic;
using System.Linq;

namespace DPML_Proj1.CSP.Model
{
    /// <summary>
    /// Domain class as enumeration of values (assume we work with finite and not too large domains)
    /// </summary>
    public class Domain
    {
        private readonly HashSet<Value> fValues;

        public IEnumerable<Value> Values => fValues;

        public int Size => fValues.Count;

        public Domain(IEnumerable<Value> values)
        {
            fValues = new HashSet<Value>(values);
        }

        public Domain(Domain domain)
        {
            fValues = new HashSet<Value>(domain.fValues);
        }

        /// <summary>
        /// Returns an integers domain between start and stop (inclusively), with a specified step
        /// </summary>
        /// <param name="start"></param>
        /// <param name="stop"></param>
        /// <param name="step"></param>
        /// <returns></returns>
        public static Domain IntRange(int start, int stop, int step = 0)
        {
            if(step==0)
            {
                step = start <= stop ? 1 : -1;
            }
            var values = new List<TypedValue<int>>();
            if (start <= stop)
            {
                for (int i = start; i <= stop; i += step)
                {
                    values.Add(new TypedValue<int>(i));
                }
            }
            else
            {
                for (int i = start; i >= stop; i += step) 
                {
                    values.Add(new TypedValue<int>(i));
                }
            }
            return new Domain(values.ToArray());
        }

        /// <summary>
        /// Domain from a collection of values
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="values"></param>
        /// <returns></returns>
        public static Domain FromValues<T>(IEnumerable<T> values)
        {
            return new Domain(values.Distinct().Select(v => new TypedValue<T>(v)));
        }

        /// <summary>
        /// Domain from string labels
        /// </summary>
        /// <param name="labels"></param>
        /// <returns></returns>
        public static Domain StringLabels(params string[] labels)
        {
            return new Domain(labels.Select(l => new TypedValue<string>(l)).ToArray());
        }
    }
}
