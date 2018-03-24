/**
 * Created by zw on 5/6/16.
 */
public class EmptyThingException extends NullPointerException {
    private static final long serialVersionUID = 42L;

    /**
     * Takes a string <code>message</code> and uses it as input
     * to its parent class to be printed to screen.
     *
     * @param message the thrown instance to be output
     */
    public EmptyThingException (String message) {
        super(message);
    }
}
