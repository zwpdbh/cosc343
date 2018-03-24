import java.util.Random;

/**
 * Created by zw on 5/8/16.
 */
public class DummyTest {
    public static void main(String[] args) {
//        int[] one = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
//        int[] two = {2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2};
//        int[] result = new int[13];
//
//        int c = 1;
//        System.arraycopy(one, 0, result, 0, c);
//        System.arraycopy(two, c, result, c, 13-c);
//        for (int i: result) {
//            System.out.print(i + " ");
//        }
        int[] one = {0,0,0, 0,0,0,0,1, 2 ,3 ,4 ,5, 6};
        System.out.println(one.length);

        Random r = new Random();
        for (int i = 0; i<200; i++) {
            int indexA = r.nextInt(6) + 7;
            int indexB = r.nextInt(6) + 7;
            while (indexA==indexB) {
                indexB = r.nextInt(6) + 7;
            }
            int tmp = one[indexA];
            one[indexA] = one[indexB];
            one[indexB] = tmp;
            for (int each: one) {
                System.out.print(each + " ");
            }
            System.out.println();
        }
    }
}
