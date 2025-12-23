
namespace DPML_Proj1.UI.Controls
{
    partial class ReducerSelector
    {
        /// <summary> 
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Component Designer generated code

        /// <summary> 
        /// Required method for Designer support - do not modify 
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.OptionsList = new System.Windows.Forms.ListBox();
            this.SelectedList = new System.Windows.Forms.ListBox();
            this.ChooseButton = new System.Windows.Forms.Button();
            this.UnchooseButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // OptionsList
            // 
            this.OptionsList.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left)));
            this.OptionsList.FormattingEnabled = true;
            this.OptionsList.Location = new System.Drawing.Point(3, 0);
            this.OptionsList.Name = "OptionsList";
            this.OptionsList.Size = new System.Drawing.Size(150, 173);
            this.OptionsList.TabIndex = 0;
            // 
            // SelectedList
            // 
            this.SelectedList.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.SelectedList.FormattingEnabled = true;
            this.SelectedList.Location = new System.Drawing.Point(248, 0);
            this.SelectedList.Name = "SelectedList";
            this.SelectedList.Size = new System.Drawing.Size(150, 173);
            this.SelectedList.TabIndex = 1;
            // 
            // ChooseButton
            // 
            this.ChooseButton.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.ChooseButton.Location = new System.Drawing.Point(186, 61);
            this.ChooseButton.Name = "ChooseButton";
            this.ChooseButton.Size = new System.Drawing.Size(31, 23);
            this.ChooseButton.TabIndex = 2;
            this.ChooseButton.Text = ">";
            this.ChooseButton.UseVisualStyleBackColor = true;
            this.ChooseButton.Click += new System.EventHandler(this.ChooseButton_Click);
            // 
            // UnchooseButton
            // 
            this.UnchooseButton.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.UnchooseButton.Location = new System.Drawing.Point(186, 90);
            this.UnchooseButton.Name = "UnchooseButton";
            this.UnchooseButton.Size = new System.Drawing.Size(31, 23);
            this.UnchooseButton.TabIndex = 3;
            this.UnchooseButton.Text = "<";
            this.UnchooseButton.UseVisualStyleBackColor = true;
            this.UnchooseButton.Click += new System.EventHandler(this.UnchooseButton_Click);
            // 
            // ReducerSelector
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.UnchooseButton);
            this.Controls.Add(this.ChooseButton);
            this.Controls.Add(this.SelectedList);
            this.Controls.Add(this.OptionsList);
            this.Name = "ReducerSelector";
            this.Size = new System.Drawing.Size(401, 182);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.ListBox OptionsList;
        private System.Windows.Forms.ListBox SelectedList;
        private System.Windows.Forms.Button ChooseButton;
        private System.Windows.Forms.Button UnchooseButton;
    }
}
