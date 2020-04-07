import javax.swing.*;
import java.awt.*;

public class Main {

    public static void main(String[] args) {
        JFrame jf = new JFrame("测试窗口");
        jf.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

        // 创建内容面板
        JPanel panel = new JPanel();

        // 表头（列名）
        String[] columnNames = {"序号", "姓名", "语文", "数学", "英语", "总分"};

        // 表格所有行数据
        Object[][] rowData = {
                {1, "张三", 80, 80, 80, 240},
                {2, "John", 70, 80, 90, 240},
                {3, "Sue", 70, 70, 70, 210},
                {4, "Jane", 80, 70, 60, 210},
                {5, "Joe_05", 80, 70, 60, 210},
                {6, "Joe_06", 80, 70, 60, 210},
                {7, "Joe_07", 80, 70, 60, 210},
                {8, "Joe_08", 80, 70, 60, 210},
                {9, "Joe_09", 80, 70, 60, 210},
                {10, "Joe_10", 80, 70, 60, 210},
                {11, "Joe_11", 80, 70, 60, 210},
                {12, "Joe_12", 80, 70, 60, 210},
                {13, "Joe_13", 80, 70, 60, 210},
                {14, "Joe_14", 80, 70, 60, 210},
                {15, "Joe_15", 80, 70, 60, 210},
                {16, "Joe_16", 80, 70, 60, 210},
                {17, "Joe_17", 80, 70, 60, 210},
                {18, "Joe_18", 80, 70, 60, 210},
                {19, "Joe_19", 80, 70, 60, 210},
                {20, "Joe_20", 80, 70, 60, 210}
        };

        // 创建一个表格，指定 表头 和 所有行数据
        JTable table = new JTable(rowData, columnNames);

        // 设置表格内容颜色
        table.setForeground(Color.BLACK);                   // 字体颜色
        table.setFont(new Font(null, Font.PLAIN, 14));      // 字体样式
        table.setSelectionForeground(Color.DARK_GRAY);      // 选中后字体颜色
        table.setSelectionBackground(Color.LIGHT_GRAY);     // 选中后字体背景
        table.setGridColor(Color.GRAY);                     // 网格颜色

        // 设置表头
        table.getTableHeader().setFont(new Font(null, Font.BOLD, 14));  // 设置表头名称字体样式
        table.getTableHeader().setForeground(Color.RED);                // 设置表头名称字体颜色
        table.getTableHeader().setResizingAllowed(false);               // 设置不允许手动改变列宽
        table.getTableHeader().setReorderingAllowed(false);             // 设置不允许拖动重新排序各列

        // 设置行高
        table.setRowHeight(30);

        // 第一列列宽设置为40
        table.getColumnModel().getColumn(0).setPreferredWidth(40);

        // 设置滚动面板视口大小（超过该大小的行数据，需要拖动滚动条才能看到）
        table.setPreferredScrollableViewportSize(new Dimension(400, 300));

        // 把 表格 放到 滚动面板 中（表头将自动添加到滚动面板顶部）
        JScrollPane scrollPane = new JScrollPane(table);

        // 添加 滚动面板 到 内容面板
        panel.add(scrollPane);

        // 设置 内容面板 到 窗口
        jf.setContentPane(panel);

        jf.pack();
        jf.setLocationRelativeTo(null);
        jf.setVisible(true);
    }

} 
