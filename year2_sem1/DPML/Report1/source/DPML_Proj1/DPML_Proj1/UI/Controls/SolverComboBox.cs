using DPML_Proj1.CSP.Solvers;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls
{
    public class SolverComboBox : ComboBox
    {
        private readonly Type[] SolverTypes = Assembly.GetExecutingAssembly()
            .GetTypes()
            .Where(t => t.IsClass && !t.IsAbstract && typeof(ICspSolver).IsAssignableFrom(t))
            .ToArray();

        public SolverComboBox()
        {
            Items.Clear();
            Items.AddRange(SolverTypes);
            SelectedIndex = 0;
            DisplayMember = nameof(Type.Name);
        }

        [DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)]
        public new ObjectCollection Items => base.Items;


    }
}
