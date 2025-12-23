using System;

namespace DPML_Proj1.CSP.Model
{
    /// <summary>
    /// Value wraps around a native C# object in order to handle it more easily inside the system.
    /// </summary>
    public abstract class Value
    {
        /// <summary>
        /// Get the actual data from the Value object casted to a desired type 
        /// (user code must ensure the cast is valid)
        /// </summary>
        /// <typeparam name="U"></typeparam>
        /// <returns></returns>
        public abstract U EvaluateAs<U>();

        public object AsObject() => EvaluateAs<object>();
    }

    public class TypedValue<T> : Value
    {
        public readonly T Data;

        public TypedValue(T data)
        {
            Data = data;
        }

        public override U EvaluateAs<U>() => (U)Convert.ChangeType(Data, typeof(U));

        public override string ToString() => Data.ToString();
    }
}
