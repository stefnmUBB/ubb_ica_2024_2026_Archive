using System;
using System.Drawing;
using System.Windows.Forms;

namespace DPML_Proj1.UI.Controls
{
    public partial class CustomTabControl : UserControl
    {
        public event EventHandler<TabCloseEventArgs> TabCloseClicked;

        public CustomTabControl()
        {
            InitializeComponent();

            TabControl.DrawMode = TabDrawMode.OwnerDrawFixed;
            TabControl.SizeMode = TabSizeMode.Normal;
            TabControl.Multiline = false;
            TabControl.Alignment = TabAlignment.Top;
            TabControl.Appearance = TabAppearance.Normal;
            TabControl.Padding = new Point(12, 3);

            TabControl.DrawItem += TabControl_DrawItem;
            TabControl.MouseDown += TabControl_MouseDown;
            TabControl.MouseMove += TabControl_MouseMove;
            TabControl.MouseLeave += TabControl_MouseLeave;
        }

        private int _hoverCloseIndex = -1;
        private const int CLOSE_SIZE = 12;
        private const int CLOSE_PADDING = 6;

        public TabControl InnerTabControl => TabControl;

        private void TabControl_DrawItem(object sender, DrawItemEventArgs e)
        {
            Graphics g = e.Graphics;
            g.SmoothingMode = System.Drawing.Drawing2D.SmoothingMode.AntiAlias;
            g.TextRenderingHint = System.Drawing.Text.TextRenderingHint.ClearTypeGridFit;

            var page = TabControl.TabPages[e.Index];
            Rectangle r = e.Bounds;

            bool selected = (TabControl.SelectedIndex == e.Index);
            Color back = selected ? ControlPaint.LightLight(SystemColors.Control) : SystemColors.ControlLight;

            using (var br = new SolidBrush(back))
                g.FillRectangle(br, r);

            // Draw text
            Rectangle textRect = r;
            textRect.Width -= (CLOSE_SIZE + CLOSE_PADDING);
            TextRenderer.DrawText(g, page.Text, TabControl.Font, textRect, SystemColors.ControlText,
                TextFormatFlags.VerticalCenter | TextFormatFlags.Left | TextFormatFlags.EndEllipsis);

            // Draw close button
            Rectangle closeRect = GetCloseRect(r);
            DrawCloseButton(g, closeRect, e.Index == _hoverCloseIndex);
        }

        private void TabControl_MouseDown(object sender, MouseEventArgs e)
        {
            for (int i = 0; i < TabControl.TabPages.Count; i++)
            {
                Rectangle r = TabControl.GetTabRect(i);
                Rectangle closeRect = GetCloseRect(r);
                if (closeRect.Contains(e.Location))
                {
                    var args = new TabCloseEventArgs(i, TabControl.TabPages[i]);
                    TabCloseClicked?.Invoke(this, args);
                    if (!args.Cancel)
                        TabControl.TabPages.RemoveAt(i);
                    return;
                }
            }
        }

        private void TabControl_MouseMove(object sender, MouseEventArgs e)
        {
            int newHover = -1;
            for (int i = 0; i < TabControl.TabPages.Count; i++)
            {
                Rectangle closeRect = GetCloseRect(TabControl.GetTabRect(i));
                if (closeRect.Contains(e.Location))
                {
                    newHover = i;
                    break;
                }
            }

            if (newHover != _hoverCloseIndex)
            {
                _hoverCloseIndex = newHover;
                TabControl.Invalidate();
            }
        }

        private void TabControl_MouseLeave(object sender, EventArgs e)
        {
            if (_hoverCloseIndex != -1)
            {
                _hoverCloseIndex = -1;
                TabControl.Invalidate();
            }
        }

        private Rectangle GetCloseRect(Rectangle tabRect)
        {
            return new Rectangle(
                tabRect.Right - CLOSE_SIZE - CLOSE_PADDING,
                tabRect.Top + (tabRect.Height - CLOSE_SIZE) / 2,
                CLOSE_SIZE,
                CLOSE_SIZE);
        }

        private void DrawCloseButton(Graphics g, Rectangle r, bool hover)
        {
            using (var b = new SolidBrush(hover ? Color.LightGray : Color.WhiteSmoke))
            using (var p = new Pen(Color.Gray))
            {
                g.FillEllipse(b, r);
                g.DrawEllipse(p, r);
            }

            using (var pen = new Pen(Color.Black, 1.5f))
            {
                g.DrawLine(pen, r.Left + 3, r.Top + 3, r.Right - 3, r.Bottom - 3);
                g.DrawLine(pen, r.Left + 3, r.Bottom - 3, r.Right - 3, r.Top + 3);
            }
        }

        public void AddTab(string title, Control content = null)
        {
            var page = new TabPage(title);
            if (content != null)
            {
                content.Dock = DockStyle.Fill;
                page.Controls.Add(content);
            }
            TabControl.TabPages.Add(page);
            TabControl.SelectedTab = page;
        }

        public void RemoveTab(int index)
        {
            if (index >= 0 && index < TabControl.TabPages.Count)
                TabControl.TabPages.RemoveAt(index);
        }

        public void ClearTabs()
        {
            TabControl.TabPages.Clear();
        }
    }

    public class TabCloseEventArgs : EventArgs
    {
        public int TabIndex { get; }
        public TabPage TabPage { get; }
        public bool Cancel { get; set; }
        public TabCloseEventArgs(int index, TabPage page)
        {
            TabIndex = index;
            TabPage = page;
        }
    }

}
