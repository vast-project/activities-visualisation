import {createContext, useContext, useState} from "react";
import Button from "@component/ui/button/Button";
import First from "../first/First";
import styles from './textAnnotation.module.css'
import {BsArrowLeftCircleFill} from 'react-icons/bs'
import Instructions from "../instructions/Instructions"
import {LangContext} from "../layout/Layout";

export const ValuesContext = createContext();

function TextAnnotations() {
    const {isEnglish, setIsEnglish} = useContext(LangContext)

    const [next, setNext] = useState(false);
    const [previous, setPrevious] = useState(false);

    const [startPos, setStartPos] = useState(-1);
    const [endPos, setEndPos] = useState(-1);
    const [tooltipComment, setTooltipComment] = useState("");
    const [comments, setComments] = useState([]);
    const [selectText, setSelectText] = useState("");

    const text =
        isEnglish ?
            (
                <div>
                    <p><strong>DOMIN:</strong> Good! And you can say whatever you like to them. You can read the Bible,
                        recite the multiplication table, whatever you please. You can even preach to them about human
                        rights.</p>
                    <p><strong>HELENA:</strong> Oh, I think that if you were to show them a little love!</p>
                    <p><strong>FABRY:</strong> Impossible, Miss Glory. Nothing is harder to like than a
                        Robot.</p>
                    <p><strong>HELENA:</strong> What do you make them for, then?</p>
                    <p><strong>BUSMAN:</strong> Ha, ha, ha, that's good! What are Robots made for?</p>
                    <p><strong>FABRY:</strong> For work, Miss Glory! One Robot can replace two and a half workmen. The
                        human machine, Miss Glory, was terribly imperfect. It had to be removed sooner or later.</p>
                    <p><strong>BUSMAN:</strong> It was too expensive.</p>
                    <p><strong>FABRY:</strong> It was not effective. It no longer answers the requirements of modern
                        engineering. Nature has no idea of keeping pace with modern labor. For example: from a technical
                        point of view, the whole of childhood is a sheer absurdity. So much time lost. And then again!
                    </p>
                    <p><strong>HELENA:</strong> Oh, no! No!</p>
                    <p><strong>FABRY:</strong> Pardon me. But kindly tell me what is the real aim of your
                        League!–– the... the Humanity League.
                    </p>
                    <p><strong>HELENA:</strong> Its real purpose is to!–– to protect the Robots!–– and!–– and
                        ensure good treatment for them.
                    </p>
                    <p><strong>FABRY:</strong> Not a bad object, either. A machine has to be treated
                        properly. Upon my soul, I approve of that. I don't like
                        damaged articles. Please, Miss Glory, enroll us all as
                        contributing, or regular, or foundation members of your
                        League.
                    </p>
                    <p><strong>HELENA:</strong> No, you don't understand me. What we really want is to!–– to
                        liberate the Robots.
                    </p>
                    <p><strong>HALLEMEIER:</strong> How do you propose to do that?</p>
                    <p><strong>HELENA:</strong> They are to be!–– to be dealt with like human beings.</p>
                    <p><strong>HALLEMEIER:</strong> Aha. I suppose they're to vote? To drink beer? to order us
                        about?
                    </p>
                    <p><strong>HELENA:</strong> Why shouldn't they drink beer?</p>
                    <p><strong>HALLEMEIER:</strong> Perhaps they're even to receive wages?</p>
                    <p><strong>HELENA:</strong> Of course they are.</p>
                    <p><strong>HALLEMEIER:</strong> Fancy that, now! And what would they do with their wages,
                        pray?
                    </p>
                    <p><strong>HELENA:</strong> They would buy!–– what they need... what pleases them...</p>
                    <p><strong>HALLEMEIER:</strong> That would be very nice, Miss Glory, only there's nothing
                        that does please the Robots. Good heavens, what are they to
                        buy? You can feed them on pineapples, straw, whatever you
                        like. It's all the same to them, they've no appetite at all.
                        They've no interest in anything, Miss Glory. Why, hang it
                        all, nobody's ever yet seen a Robot smile.
                    </p>
                </div>
            )
            :
            (
                <div>
                    <p><strong>ΝΤΟΜΙΝ:</strong> Ωραία. Μπορείτε να τους πείτε ό,τι θέλετε. Μπορείτε να τους διαβάσετε τη
                        Βίβλο, λογάριθμους ή ότι σας αρέσει. Μπορείτε ακόμα να τους κάνετε κήρυγμα και για τα ανθρώπινα
                        δικαιώματα.</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Ω, πιστεύω πως…άμα τους δείξει κάποιος λίγη αγάπη…</p>
                    <p><strong>ΦΑΜΠΡΥ:</strong> Αδύνατον, δεσποινίς Γκλόρυ. Τίποτα δεν διαφέρει από τον άνθρωπο τόσο όσο
                        το ρομπότ.</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Τότε γιατί τα φτιάχνετε;</p>
                    <p><strong>ΜΠΟΥΣΜΑΝ:</strong> Χα, χα, χα! Ωραίο είν΄ αυτό! Γιατί φτιάχνουμε ρομπότ!</p>
                    <p><strong>ΦΑΜΠΡΥ:</strong> Για να δουλεύουν, δεσποινίς. Ένα ρομπότ αντικαθιστά δυόμισι εργάτες. Η
                        ανθρώπινη μηχανή, δεσποινίς Γκλόρυ, ήταν απίστευτα ατελής. Έπρεπε κάποτε να πραμεριστεί.</p>
                    <p><strong>ΜΠΟΥΣΜΑΝ:</strong> Ήτανε πανάκριβη.</p>
                    <p><strong>ΦΑΜΠΡΥ:</strong> Είχε μικρή αποδοτικότητα. Δεν μπορούσε ν' ανταποκριθεί πλέον στη
                        σύγχρονη τεχνολογία. Και δεύτερον... και δεύτερον... ειναι μεγαλη προοδος που... Με συγχωρείτε.
                    </p>
                    <p><strong>ΕΛΕΝΑ:</strong> Για ποιο πράγμα;</p>
                    <p><strong>ΦΑΜΠΡΥ:</strong> Ζητώ συγγνώμη, αλλά είναι μεγάλη πρόοδος να γεννάς με μία μηχανή. Είναι
                        πιο άνετο και πιο γρήγορο. Κάθε επιτάχυνση είναι πρόοδος, δεσποινίς. Η φύση, δεν είχε ιδέα από
                        τον σύγχρονο ρυθμό εργασίας. Ολόκληρη η παιδική ηλικία, από τεχνική άποψη, είναι μια καθαρή
                        βλακεία. Πέρα για πέρα χαμένος χρόνος. Ανυπόφορη σπατάλη χρονου, δεσποινίς Γκλόρυ. Και τρίτον
                        ...</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Ω, σταματήστε!</p>
                    <p><strong>ΦΑΜΠΡΥ:</strong> Με συγχωρείτε! Επιτρέψτε μου, δεσποινίς, τι επιδιώκει αυτή η Λίγκα σας …
                        Λίγκα... πώως την είπατε … ανθρωπιστική Λίγκα;</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Επιδιώκει κυρίως… κυρίως πρέπει να προστατεύσει τα ρομποτ και… και... να
                        τους... εξασφαλίσει μια καλή μεταχείριση.</p>
                    <p><strong>ΦΑΜΠΡΥ:</strong> Δεν ειναι κακοί οι στόχοι της. Τη μηχανή πρέπει να τη μεταχειριζόμαστε
                        καλά. Σας βεβαιώ, μ' ενθουσιάζει. Δεν μ' αρέσούν τα χαλασμένα πράματα. Σας παρακαλώ λοιπόν,
                        δεσποινίς Γκλόρυ, γράψτε μας όλους ως αντεπιστελλοντα, ως τακτικά, ως ιδρυτικά μέλη στη Λίγκα
                        σας!</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Όχι, δεν με καταλαβαίνετε. Θέλουμε... κυρίως... θέλουμε ν'
                        απελευθερώσουμε τα ρομπότ!</p>
                    <p><strong>ΧΑΛΛΕΜΑΓΙΕΡ:</strong> Πώς είπατε;</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Πρέπει να τα... μεταχειριζόμαστε σαν ανθρώπους.</p>
                    <p><strong>ΧΑΛΛΕΜΑΓΙΕΡ:</strong> Αχά! Μήπως πρέπει και να ψηφίζουν; Να πίνουν μπύρα; Να σας
                        διατάζουν;</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Γιατί να μην ψηφίζουν;</p>
                    <p><strong>ΧΑΛΛΕΜΑΓΙΕΡ:</strong> Μήπως θα πρέπει να παίρνουν και μισθό, τελικά;</p>
                    <p><strong>ΕΛΕΝΑ:</strong> Βεβαίως!</p>
                    <p><strong>ΧΑΛΛΕΜΑΓΙΕΡ:</strong> Για κοιτάτε, ρε παιδιά! Και τι θα τον κάνουν τον μισθό παρακαλώ;
                    </p>
                    <p><strong>ΕΛΕΝΑ:</strong> Θ' αγοράζουνε... ό,τι τους χρειάζεται... ό,τι τους κάνει κέφι.</p>
                    <p><strong>ΧΑΛΛΕΜΑΓΙΕΡ:</strong> Πολύ ωραίο αυτό, δεσποινίς μου, μόνο που στα ρομπότ τίποτα δεν
                        χάνει κέφι. Για το Θεό, τι ν' αγοράσουνε; Μπορείτε να τα ταΐσετε ανανάδες, σανό, οτιδήποτε
                        θέλετε, τους είναι αδιάφορο, δεν έχουν καθόλου όρεξη.</p>
                </div>
            );

    const handleTextClick = (e) => {
        const selection = window.getSelection();
        setSelectText(selection.toString());
        console.log(selection.toString())
        if (selection.toString()) {
            const commentObj = {text: selection.toString(), value: tooltipComment};
            // setComments([...comments, commentObj]);
            setTooltipComment("");
        }
    };

    /**
     * Delete the annotation with the given index
     * @param index The index of the annotation to delete
     */
    const deleteAnnotation = (index) => {
        const newComments = [...comments];
        newComments.splice(index, 1);
        setComments(newComments);
    }

    /**
     * Handle changes in the text area of the tooltip (where the user writes the value)
     * @param e
     */
    const handleTooltipChange = (e) => {
        setTooltipComment(e.target.value);
    };

    const renderSelectedText = () => {
        if (selectText) {
            // const selectedText = text.slice(startPos, endPos);
            return <span className={styles.selectedText}>"{selectText}"</span>;
        }
        return null;
    };

    const renderComments = () => {
        if (comments.length > 0) {
            return (
                <div className={styles.valueContainer}>
                    <h3 className={styles.valueTitle}>{isEnglish ? 'VALUES' : 'ΑΞΙΕΣ'}</h3>
                    <ul className={styles.commentsList}>
                        {comments.map((commentObj, index) => (
                            <li className={styles.commentsItem} key={index}>
                                <div className={styles.commentsItemColumn}>
                                    <div className={styles.commentsValue}>{commentObj.comment}</div>
                                    <div className={styles.commentsText}>"{commentObj.text}"</div>
                                </div>
                                <div className={styles.commentsItemColumn}>
                                    <span onClick={() => deleteAnnotation(index)}
                                          className={styles.commentsDelete}>🗑️</span>
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>
            );
        }
        return null;
    };

    if (next) {
        return <First selectedWordsArray={comments}/>
    }
    if (previous) {
        return (
            <ValuesContext.Provider value={comments}>
                <Instructions/>
            </ValuesContext.Provider>
        )
    }

    return (
        <div className={styles.container}>
            <BsArrowLeftCircleFill onClick={() => setPrevious(true)} className={styles.leftArrow}/>
            <h2>{isEnglish ? 'Text' : 'Κειμενο'}</h2>
            <div className={styles.text} onClick={handleTextClick}>{text}</div>
            {renderSelectedText()}
            {selectText && (
                <Tooltip
                    isEnglish={isEnglish}
                    comment={tooltipComment}
                    onChange={handleTooltipChange}
                    onSave={() => {
                        if (!selectText || !tooltipComment) {
                            setTooltipComment("");
                            setSelectText("");
                            return;
                        }
                        const commentObj = {text: selectText, comment: tooltipComment};
                        setComments([...comments, commentObj]);
                        setTooltipComment("");
                        setSelectText("");
                    }
                    }
                    onCancel={() => {
                        setTooltipComment("");
                        setSelectText("");
                    }}
                />
            )}

            {renderComments()}
            <Button onClick={() => setNext(!next)} color="#5C47C2" title={isEnglish ? 'NEXT' : 'ΕΠΟΜΕΝΟ'}/>
        </div>
    );
};

const Tooltip = ({comment, onChange, onSave, onCancel, isEnglish}) => {
    return (
        <div className={styles.tooltip}>
            <textarea className={styles.tooltipTextarea} value={comment} onChange={onChange}/>
            <div className={styles.btnContainer}>
                <button className={styles.tooltipBtn}
                        onClick={onSave}>{isEnglish ? 'Add Value' : 'Προσθήκη Αξίας'}</button>
                <button className={styles.tooltipCancelBtn}
                        onClick={onCancel}>{isEnglish ? 'Cancel' : 'Ακύρωση'}</button>
            </div>
        </div>
    );
};

export default TextAnnotations;
