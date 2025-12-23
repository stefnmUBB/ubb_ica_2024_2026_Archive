using DPML_Proj1.Core;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls
{
    public partial class ProblemGeneratorsListViewer : UserControl
    {
        private readonly List<ProblemGenerator> Items = typeof(ProblemGeneratorTemplates)
           .GetFields(BindingFlags.Public | BindingFlags.Static)
           .Where(f => typeof(ProblemGenerator).IsAssignableFrom(f.FieldType))
           .Select(f => f.GetValue(null) as ProblemGenerator)
           .ToList();

        public ProblemGeneratorsListViewer()
        {
            InitializeComponent();
            ListBox.DataSource = Items;
            ListBox.DisplayMember = nameof(ProblemGenerator.Name);
            ListBox.DoubleClick += ListBox_DoubleClick;
        }

        private void ListBox_DoubleClick(object sender, EventArgs e)
        {
            if (ListBox.SelectedItem is ProblemGenerator selected)
            {
                ProblemGeneratorSelected?.Invoke(this, selected);
            }
        }

        public event EventHandler<ProblemGenerator> ProblemGeneratorSelected;
    }
}
