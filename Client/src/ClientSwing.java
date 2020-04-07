import javax.swing.*;
import javax.swing.table.*;
import java.awt.*;
import java.awt.event.*;

import java.net.Socket;
import java.util.Scanner;
import java.io.PrintStream;
import java.io.FileOutputStream;
import java.io.File;
import java.io.IOException;

 class PA_Client{
    Socket client;
    Scanner in;
    PrintStream out;
    public PA_Client(){}
    public void connect(String ip, int port)throws Exception{
        this.client = new Socket(ip, port);
        this.in = new Scanner(client.getInputStream());
        this.in.useDelimiter(";");
        this.out = new PrintStream(client.getOutputStream());
        System.out.println("监控客户端启动\n已连接服务器，IP地址：" + client.	getInetAddress() + "\n");
    }
    public void close() throws Exception{
        this.out.println("exit");      //发送关闭连接指令
        this.client.shutdownInput();
        this.client.shutdownOutput();
        this.client.close();
        System.out.println("服务器断开连接");
    }
        
    public StringBuffer startWatch(int row)throws Exception{
        File file = new File("./test_data/base.tmp");
        if(!file.getParentFile().exists()){
            file.getParentFile().mkdirs();
        }
        if(!file.exists()){
            file.createNewFile();
        }
        PrintStream writefile = new PrintStream(new FileOutputStream(file));
        
        this.out.println(row);       //发送要读取的日志行数
        if(this.in.hasNext()){       //阻塞等待输入
            writefile.println(this.in.next());  //输出到缓存文件
            if(this.processData(row)){          //预处理数据
                return this.analyzeData();             //分析数据
            }
        }
        return null;
    }
    
    //预处理数据
    private boolean processData(int row) throws Exception{
        String cmd = "./process_test_data.py " + String.valueOf(row);
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor() != 0){
            System.out.println("数据处理失败");
            return false;
        }
        return true;
    }
    
    //机器学习模型分析数据
    private StringBuffer analyzeData() throws Exception{
        String cmd = "./test_pa.py";
        Runtime runtime = Runtime.getRuntime();
        Process process = runtime.exec(cmd);
        if(process.waitFor() != 0){
            System.out.println("数据计算失败");
            return null;
        }
        Scanner scan = new Scanner(process.getInputStream());
        scan.useDelimiter("\n");
        
        StringBuffer buf = new StringBuffer();
        while(scan.hasNext()){
            String str = scan.next(); 
            buf.append(str);
            System.out.println(str);
        }
        scan.close();
        return buf;
    }
    
    public void timer(int s)throws Exception{
        while((s--) > 0){
            System.out.printf("等待服务器搜集日志信息:%2ds\r", s);
            Thread.sleep(1000);
        }
        System.out.println("\n");
    }
    public static void main(String args[]){
        PA_Client c = new PA_Client();
        try{
            c.connect("localhost",5973);
            //c.timer(30);
            System.out.println(c.startWatch(10) + "1");
        }catch(Exception e){
            System.out.println(e);
        }finally{
            try{
                c.close();
            }catch(Exception e){
                System.out.println(e);
            }
        }
    }
}

public class ClientSwing {
    private JFrame frame;
    private JPanel panel;    
    private JLabel ipLabel;
    private JLabel portLabel;
    private JLabel timeLabel;
    private JLabel cntLabel;
    private JLabel statusLabel;
    private JTextField ipText;
    private JTextField portText;      
    private JTextField timeText;
    private JTextField cntText;
    private JButton startButton;
    private JButton connectButton;
    private int connect_status;
    private int test_status;
    private PA_Client client;
    private JTable table;
    
    private ClientSwing(){
        this.frame = new JFrame("电力攻击检测客户端");
        this.panel = new JPanel(null);    
        this.ipLabel = new JLabel("服务器IP地址：");
        this.portLabel = new JLabel("端口：");
        this.timeLabel = new JLabel("时间间隔(s)：");
        this.cntLabel = new JLabel("次数：");
        this.statusLabel = new JLabel("(未连接)");
        this.ipText = new JTextField("127.0.0.1",15);
        this.portText = new JTextField("5973",4);       
        this.timeText = new JTextField("60",3);
        this.cntText = new JTextField("10",3);
        this.startButton = new JButton("开始");
        this.connectButton = new JButton("连接");
        this.client = new PA_Client();
        this.connect_status = 0;
        this.test_status = 0;
    }
    private void init(){
        this.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.frame.setSize(550,500);
        placeComponents();
        placeTable();
        setButtunAction();
        
        this.frame.add(this.panel);
        this.frame.setContentPane(this.panel);
        this.frame.setLocationRelativeTo(null);
        this.frame.setVisible(true);
    }
    private  void placeComponents() {
    
        this.ipLabel.setBounds(20,20,90,30);
        this.timeLabel.setBounds(20,60,90,30);
        
        this.ipText.setBounds(110,20,100,30);
        this.timeText.setBounds(110,60,100,30);
        
        this.portLabel.setBounds(220,20,50,30);
        this.cntLabel.setBounds(220,60,50,30);
        
        this.portText.setBounds(270,20,60,30);
        this.cntText.setBounds(270,60,60,30);
        
        this.statusLabel.setBounds(340,20,50,30);
        this.connectButton.setBounds(400,20,70,30);
        this.startButton.setBounds(400,60,70,30);
       
        this.panel.add(this.ipLabel);
        this.panel.add(this.ipText);
        this.panel.add(this.portLabel);
        this.panel.add(this.portText);
        this.panel.add(this.connectButton);
        this.panel.add(this.timeLabel);
        this.panel.add(this.timeText);
        this.panel.add(this.cntLabel);
        this.panel.add(this.cntText);
        this.panel.add(this.startButton);
        this.panel.add(this.statusLabel);
    }
    private void placeTable(){
        DefaultTableModel model = new DefaultTableModel();
        model.addColumn("Code");
        model.addColumn("Name");
        model.addColumn("Quantity");
        model.addColumn("Unit Price");
        model.addColumn("Price");
        this.table = new JTable(model);
        table.setPreferredScrollableViewportSize(new Dimension(400, 250));
        JScrollPane scpanel = new JScrollPane(this.table);
        scpanel.setBounds(75,150,400,300);
        this.panel.add(scpanel);
    }
    public void setButtunAction(){
        this.connectButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                connect_status ++;
                try{
                    if(connect_status%2==1){
                        String ip = ipText.getText();
                        int port = Integer.valueOf(portText.getText());
                        client.connect(ip, port);
                        statusLabel.setText("(已连接)");
                        connectButton.setText("断开");
                    }
                    else{
                        client.close();
                        statusLabel.setText("(已断开)");
                        connectButton.setText("连接");
                    }
                }catch(Exception ex){
                    if(connect_status%2==1){
                        statusLabel.setText("(连接失败)");
                    }else{
                        statusLabel.setText("(断开失败)");
                    }
                    System.out.println(ex);
                }
            }
        });
        this.startButton.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e){
                test_status++;
                try{
                    if(test_status%2==1){
                        startButton.setText("停止");
                        int time = Integer.valueOf(timeText.getText());
                        int n = Integer.valueOf(timeText.getText());
                        int cnt = 0;
                        while((cnt++)<n && test_status%2==1){
                            client.timer(time);
                            StringBuffer buf =  client.startWatch(time/3);
                            TableModel tm = table.getModel();
                            if(tm instanceof DefaultTableModel){
                                tm.addRow(new Object[]{cnt, buf.toString(), "Boss"});
                            }
                        }
                    }else{
                        startButton.setText("开始");
                    }
                }catch(Exception ex){
                    System.out.println(ex);
                }
            }
        });    
    }
    public static void main(String[] args) {    
        new ClientSwing().init();
    }
}
