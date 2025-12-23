namespace DPML_Proj1.CSP.Model
{
    /// <summary>
    /// Declared variable object with its domain
    /// </summary>
    public class Variable
    {
        public readonly string Name;
        public readonly Domain Domain;

        public Variable(string name, Domain domain)
        {
            Name = name;
            Domain = domain;
        }

        public override string ToString() => $"Variable{{{Name}, {Domain}}}";
    }
}
