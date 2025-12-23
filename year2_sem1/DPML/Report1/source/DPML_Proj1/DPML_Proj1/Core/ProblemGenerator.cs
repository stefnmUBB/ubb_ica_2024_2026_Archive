using DPML_Proj1.CSP.Model;
using DPML_Proj1.UI.Controls.SolutionViewers;
using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace DPML_Proj1.Core
{
    /// <summary>
    /// This class defines allows for defining parameterized CSP problems.
    /// For example, for a CSP problem that happens on a NxM board (such as knight tour),
    /// a ProblemGenerator can be defined to use 2 parameters N,M and provide a method that
    /// for concrete value of those parameters create the suitable problem
    /// </summary>
    public class ProblemGenerator
    {
        public readonly Dictionary<string, Type> ParameterTypes = new Dictionary<string, Type>();
        public readonly Dictionary<string, object> ParameterValues = new Dictionary<string, object>();
        public readonly Type SolutionViewerType;
        private readonly Func<ParamAccess, Problem> fGenerator;
        private readonly ParamAccess paramAccess;
        
        public string Name { get; set; }
        public string Description { get; set; }

        public ProblemGenerator(
            Dictionary<string, Type> parameterTypes,
            Dictionary<string, object> defaultValues,
            Func<ParamAccess, Problem> generator,
            string name = null,
            string description = null,
            Type solutionViewerType = null
            )
        {
            ParameterTypes = parameterTypes;
            ParameterValues = defaultValues;
            fGenerator = generator;
            SolutionViewerType = solutionViewerType;
            paramAccess = new ParamAccess(this);
            Name = name ?? "(no name)";
            Description = description ?? "";
        }

        public bool HasParameters() => ParameterTypes.Count > 0;

        // this is used inside the factory class
        public class ParamAccess
        {
            private readonly ProblemGenerator Generator;

            public ParamAccess(ProblemGenerator generator)
            {
                Generator = generator;
            }

            public T Get<T>(string key)
            {
                if(!Generator.ParameterTypes.ContainsKey(key))
                {
                    throw new InvalidOperationException($"Could not get parameter {key}");
                }

                if(!Generator.ParameterValues.ContainsKey(key))
                {
                    return default;
                }

                var value = Generator.ParameterValues[key];

                if(value==null)
                {
                    return default;
                }

                if(typeof(T).IsAssignableFrom(value.GetType()))
                {
                    return (T)value;
                }

                throw new InvalidOperationException($"Parameter type mismatch: excpected {typeof(T)}, got {value.GetType()}");
            }
        }

        public Problem GenerateProblem() => fGenerator(paramAccess);

        public T GeParam<T>(string key)
        {
            if (!ParameterTypes.ContainsKey(key))
            {
                throw new InvalidOperationException($"Could not get parameter {key}");
            }

            if (!ParameterValues.ContainsKey(key))
            {
                return default;
            }

            var value = ParameterValues[key];

            if (value == null)
            {
                return default;
            }

            if (typeof(T).IsAssignableFrom(value.GetType()))
            {
                return (T)value;
            }

            throw new InvalidOperationException($"Parameter type mismatch: excpected {typeof(T)}, got {value.GetType()}");
        }
    }

    // factory class
    public class ProblemGeneratorBuilder
    {
        private readonly Dictionary<string, Type> ParameterTypes = new Dictionary<string, Type>();
        private readonly Dictionary<string, object> DefaultValues = new Dictionary<string, object>();
        private string description = "";
        private string name = "";
        private Type ViewerControlType = null;


        public ProblemGeneratorBuilder Param<T>(string name)
        {
            ParameterTypes[name] = typeof(T);
            return this;
        }

        public ProblemGeneratorBuilder Param<T>(string name, T defaultValue)
        {
            ParameterTypes[name] = typeof(T);
            DefaultValues[name] = defaultValue;
            return this;
        }

        public ProblemGeneratorBuilder Name(string name)
        {
            this.name = name;
            return this;
        }

        public ProblemGeneratorBuilder Description(string description)
        {
            this.description = description;
            return this;
        }

        public ProblemGeneratorBuilder Viewer<V>() where V:Control, ISolutionViewer, new()
        {
            ViewerControlType = typeof(V);
            return this;
        }

        public ProblemGenerator Build(Func<ProblemGenerator.ParamAccess, Problem> generator)
        {
            return new ProblemGenerator(ParameterTypes, DefaultValues, generator,
                name: name, description: description,
                solutionViewerType: ViewerControlType);
        }
    }
}
