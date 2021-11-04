import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.json.JSONObject;
import org.json.JSONArray;

import javax.imageio.ImageIO;
import javax.swing.*;


public class Main {

    private static int current_page = 0;
    private static ShowingWindowFrame globalFrame;

    public static void main(String[] args) throws IOException {
        // make JSONArray of server answer content as a result of sending post request
        InputWindowFrame iwf = new InputWindowFrame(-1, -1);

    }

    static class InputWindowFrame{
        JFrame window_frame = new JFrame();
        int X_SIZE = 600;
        int Y_SIZE = 800;


        Object[] res_array;
        JTextField InputArray1 = new JTextField("");
        JTextField InputArray2 = new JTextField("");
        JTextField InputSr = new JTextField("");
        JTextField InputTrueValue = new JTextField("");

        public InputWindowFrame(int input_X_SIZE, int input_Y_SIZE) {

            if (input_X_SIZE > 0){
                X_SIZE = input_X_SIZE;
            }
            if (input_Y_SIZE > 0){
                Y_SIZE = input_Y_SIZE;
            }
            window_frame.setBounds(0, 0, X_SIZE, Y_SIZE);
            window_frame.setVisible(true);
            window_frame.setTitle("Ввод данных");

            JPanel panel = new JPanel();
            panel.setLayout(new BorderLayout());

            panel.add(
                    new JLabel("Массивы даных :"),
                    BorderLayout.PAGE_START
            );

            JPanel listPane = new JPanel();

            listPane.setLayout(new BoxLayout(listPane, BoxLayout.Y_AXIS));

            listPane.add(new JLabel("\tВведите 1 массив (Числа через пробел) :"));

            listPane.add(InputArray1);
            listPane.add(new JLabel("\tВведите 2 массив (если имеется) (Числа через пробел) :"));

            listPane.add(InputArray2);
            listPane.add(new JLabel("Введите Sr методики (если имеется) :"));

            listPane.add(InputSr);
            listPane.add(new JLabel("Введите истинное значение (если имеется) :"));

            listPane.add(InputTrueValue);
            JButton ConfirmButton = new JButton("Подтвердить");
            ConfirmButton.addActionListener(new ButtonConfirmListner());

            panel.add(listPane);
            panel.add(ConfirmButton, BorderLayout.PAGE_END);

            window_frame.setContentPane(panel);
            window_frame.setVisible(true);
        }

        class ButtonConfirmListner implements  ActionListener {
            public void actionPerformed (ActionEvent e) {

                String[] arr1_string = InputArray1.getText().split(" ");
                double[] arr1_double = new double[arr1_string.length];
                for(int i = 0; i < arr1_double.length; i++){
                    arr1_double[i] = Double.parseDouble(arr1_string[i].replace(",", " "));
                }
                ;

                String[] arr2_string = InputArray2.getText().split(" ");
                double[] arr2_double = new double[arr2_string.length];
                double[] arr2;
                if (!arr2_string[0].equals("")){
                    for(int i = 0; i < arr2_double.length; i++){
                        arr2_double[i] = Double.parseDouble(arr2_string[i]);
                    }
                    arr2 = arr2_double;
                } else {
                    arr2 = new double[]{};
                }

                String type;
                if (arr2.length > 0){
                    type = "2_arr";
                } else {
                    type = "1_arr";
                }

                double sr_meth = -100;
                if (!InputSr.getText().equals("")){
                    sr_meth = Double.parseDouble(InputSr.getText());
                }

                double true_value = -100;
                if (!InputTrueValue.getText().equals("")){
                    true_value = Double.parseDouble(InputTrueValue.getText());
                }

                String params = generate_params(
                        arr1_double,
                        arr2,
                        sr_meth,
                        true_value,
                        new String[]{"make_text", "make_hist", "make_boxplot"},
                        type
                );

                String res_server_str =
                        String.valueOf(
                                executePost(
                                        "http://127.0.0.1:8000",
                                        params
                                )
                        );

                JSONObject res_json = new JSONObject(res_server_str);

                if (res_json.get("status").equals("ok")) {
                    try {
                        res_array = array_to_jpanel((JSONArray) res_json.get("answer")).toArray();
                    } catch (IOException ioException) {
                        ioException.printStackTrace();
                    }
                }


                globalFrame = new ShowingWindowFrame(
                        window_frame,
                        res_array,
                        -1,
                        -1);

                globalFrame.UpdateWindoeFrame(current_page);
            }

        }
    }

    static class ShowingWindowFrame {
        JFrame window_frame;
        Object[] window_panels;
        int X_SIZE = 600;
        int Y_SIZE = 800;

        public ShowingWindowFrame(JFrame input_window_frame, Object[] input_panels, int input_X_SIZE, int input_Y_SIZE) {
            window_panels = input_panels;
            if (input_X_SIZE > 0){
                X_SIZE = input_X_SIZE;
            }
            if (input_Y_SIZE > 0){
                Y_SIZE = input_Y_SIZE;
            }
            window_frame = input_window_frame;
            window_frame.setLayout(new BorderLayout());

            window_frame.setBounds(0, 0, X_SIZE, Y_SIZE);
            window_frame.setVisible(true);
        }

        public void UpdateWindoeFrame(int i){
            window_frame.setTitle("Страница " + (i+1) + " из " + window_panels.length);
            Container new_pane = window_frame.getContentPane();
            new_pane.removeAll();

            JButton button_prew = new JButton("Назад");
            button_prew.setEnabled(false);
            if (i != 0) {
                button_prew.setEnabled(true);
                button_prew.addActionListener(new ButtonPrewListner());
            }
            new_pane.add(button_prew, BorderLayout.PAGE_START);

            new_pane.add((Component) window_panels[i], BorderLayout.CENTER);

            JButton button_next = new JButton("Далее");
            button_next.setEnabled(false);
            if (i < window_panels.length -1) {
                button_next.setEnabled(true);
                button_next.addActionListener(new ButtonNextListner());
            }
            new_pane.add(button_next, BorderLayout.PAGE_END);

            window_frame.setContentPane(new_pane);
        }
    }

    static class ButtonPrewListner implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            if (current_page -1 > -1){
                current_page -= 1;
                globalFrame.UpdateWindoeFrame(current_page);
            }
        }
    }

    static class ButtonNextListner implements ActionListener {
        public void actionPerformed (ActionEvent e) {
            if (current_page +1 < globalFrame.window_panels.length){
                current_page += 1;
                globalFrame.UpdateWindoeFrame(current_page);
            }
        }
    }

    static String generate_params(
            double[] arr1, double[] arr2, double sr_met, double true_value, String[] needed_params, String type){
        // check if involved parameters are allowed to send
        String[] req_params_1_arr = {"make_text", "make_hist", "make_boxplot"};
        String[] req_params_2_arr = {"make_text", "make_boxplot"};

        String[] curr_req_params = new String[0];
        String postfix = "";
        StringBuilder param_sum = new StringBuilder();
        if (type.equals("2_arr")) {
            curr_req_params = req_params_2_arr;
            postfix = ",\"req_type\": \"2_arr\"}";
            param_sum = new StringBuilder(
                    "{\"arr1\": " +
                    arr_to_python_str(arr1) +
                    ", \"arr2\": " +
                    arr_to_python_str(arr2) +
                    ",");
        }
        else if (type.equals("1_arr")){
            curr_req_params = req_params_1_arr;
            postfix = ",\"req_type\": \"1_arr\"}";

            postfix = ",\"sr_met\":" + sr_met + postfix;
            postfix = ",\"true_value\":" + true_value + postfix;

            param_sum = new StringBuilder("{\"arr_data\": " + arr_to_python_str(arr1) + ",");
        }

        // converting all parameters to the completed string
        for (String prm: curr_req_params){
            String str;
            if (Arrays.asList(needed_params).contains(prm)){
                str = "\"" + prm + "\":1,";
            }
            else {
                str = "\"" + prm + "\":0,";
            }
            param_sum.append(str);
        }
        param_sum = new StringBuilder(param_sum.substring(0, param_sum.length() - 1));
        return param_sum + postfix;
    }

    static String arr_to_python_str(double[] arr){
        // converting arr to the parameter for post request
        StringBuilder sum = new StringBuilder("[");
        for (double v : arr) {
            sum.append(v).append(", ");
        }
        return sum.substring(0, sum.length()-2) + "]";
    }

    static List<JPanel> array_to_jpanel(JSONArray res_array) throws IOException {

        int t_w = 500;
        int t_h = 700;

        int i_w = 580;
        int i_h = 350 * 2;

        double scale = 0.65;

        List<JPanel> jPanels = new ArrayList<>();

        for (int i = 0; i < res_array.length(); i++) {

            // JPanel is created for each JSONObject
            JSONObject row = (JSONObject) res_array.get(i);
            String row_type = (String) row.get("type");
            String row_content = (String) row.get("content");

            if (row_content.length() > 0) {

                JFrame frame = new JFrame();
                if (row_type.equals("image")) {
                    frame.setSize(i_w, i_h);
                    BufferedImage img = B64_to_BI(row_content, scale);
                    JPanel panel = panel_from_image(img);
                    jPanels.add(panel);
                }
                if (row_type.equals("text")){
                    frame.setSize(t_w, t_h);
//                    frame.setLayout(new GridLayout());

                    // a bit of text formatting with html tags
                    String formatted_text =
                            "<html>" +
                            row_content.replace(
                                "\n",
                                "<br>")
                            .replace(
                                "\t",
                                "&nbsp;&nbsp;&nbsp;"
                            ) +
                            "<html/>";

                    JPanel panel = new JPanel();
                    panel.add(
                            new JLabel(
                                    formatted_text,
                                    SwingConstants.LEFT
                            )
                    );
                    jPanels.add(panel);
                }
            }
        }
        return jPanels;
    }

    static JPanel panel_from_image(BufferedImage img){
        // returns JPanel with image involved

        return new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                g.drawImage(img, 0, 50, null);
            }
        };
    }

    static BufferedImage B64_to_BI(String png_text, double scale) throws IOException {
        // make BufferedImage from base64 string
        byte[] imageBytes = javax.xml.bind.DatatypeConverter.parseBase64Binary(png_text);
        BufferedImage img = ImageIO.read(new ByteArrayInputStream(imageBytes));

        int w = img.getWidth();
        int h = img.getHeight();

        // smoothly scaling the image
        BufferedImage after = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        AffineTransform at = new AffineTransform();
        at.scale(scale, scale);
        AffineTransformOp scaleOp =
                new AffineTransformOp(at, AffineTransformOp.TYPE_BILINEAR);
        after = scaleOp.filter(img, after);
        return after;
    }

    static String executePost(String address, String urlParameters) {
        HttpURLConnection connection = null;

        try {
            //Create connection
            URL url = new URL(address);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type",
                    "application/x-www-form-urlencoded");

            connection.setRequestProperty("Content-Length",
                    Integer.toString(urlParameters.getBytes().length));
            connection.setRequestProperty("Content-Language", "en-US");

            connection.setUseCaches(false);
            connection.setDoOutput(true);

            //Send request
            DataOutputStream wr = new DataOutputStream (
                    connection.getOutputStream());
            wr.writeBytes(urlParameters);
            wr.close();

            //Get Response
            InputStream is = connection.getInputStream();
            BufferedReader rd = new BufferedReader(new InputStreamReader(is));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = rd.readLine()) != null) {
                response.append(line);
                response.append('\r');
            }
            rd.close();
            return response.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
