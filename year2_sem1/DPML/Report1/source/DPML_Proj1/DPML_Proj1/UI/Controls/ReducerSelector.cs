using DPML_Proj1.CSP.Reducers;
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
    public partial class ReducerSelector : UserControl
    {
        private readonly Type[] ReducerTypes = Assembly.GetExecutingAssembly()
            .GetTypes()
            .Where(t => t.IsClass && !t.IsAbstract && typeof(IReducer).IsAssignableFrom(t))
            .ToArray();

        public ReducerSelector()
        {
            InitializeComponent();

            OptionsList.Items.Clear();
            OptionsList.Items.AddRange(ReducerTypes);
            OptionsList.DisplayMember = nameof(Type.Name);

            SelectedList.Items.Clear();
            SelectedList.DisplayMember = nameof(Type.Name);

        }

        private void ChooseButton_Click(object sender, EventArgs e)
        {
            var sel = OptionsList.SelectedItem;

            if(sel!=null)
            {
                OptionsList.Items.Remove(sel);
                SelectedList.Items.Add(sel);
            }
        }

        private void UnchooseButton_Click(object sender, EventArgs e)
        {
            var sel = SelectedList.SelectedItem;

            if (sel != null)
            {
                SelectedList.Items.Remove(sel);
                OptionsList.Items.Add(sel);
            }
        }

        public IReducer[] SelectedReducers => SelectedList.Items.Cast<Type>().Select(t => Activator.CreateInstance(t) as IReducer).ToArray();
    }
}
