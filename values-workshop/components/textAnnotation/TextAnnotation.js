import { useState,useRef } from "react";
import Button from "@component/ui/button/Button";
import First from "../first/First";
import styles from './textAnnotation.module.css'

function TextAnnotations({userid}) {
    const [next, setNext] = useState(false);

    const [startPos, setStartPos] = useState(-1);
    const [endPos, setEndPos] = useState(-1);
    const [tooltipComment, setTooltipComment] = useState("");
    const [comments, setComments] = useState([]);
    const text = "Ντομίν: Ωραία. Μπορείτε να τους πείτε ό,τι θέλετε. Μπορείτε να τους διαβάσετε τη Βίβλο, λογάριθμους ή ότι σας αρέσει. Μπορείτε ακόμα να τους κάνετε κήρυγμα και για τα ανθρώπινα δικαιώματα."
  
    const handleTextClick = (e) => {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        if (startPos === -1) {
          setStartPos(range.startOffset);
        } else {
          setEndPos(range.endOffset);
          const selectedText = range.toString();
          if (selectedText) {
            const commentObj = { text: selectedText, value: tooltipComment };
            setComments([...comments, commentObj]);
            setTooltipComment("");
            setStartPos(-1);
            setEndPos(-1);
          }
        }
      }
    };
  
    const handleTooltipChange = (e) => {
      setTooltipComment(e.target.value);
    };
  
    const renderSelectedText = () => {
      if (startPos !== -1 && endPos !== -1) {
        const selectedText = text.slice(startPos, endPos);
        return <span className={styles.selectedText}>"{selectedText}"</span>;
      }
      return null;
    };


    const renderComments = () => {
        console.log(comments);
        if (comments.length > 0) {
          return (
            <div className={styles.valueContainer}>
              <h3 className={styles.valueTitle}>ΑΞΙΕΣ</h3>
              <ul className={styles.commentsList}>
                {comments.map((commentObj, index) => (
                  <li className={styles.commentsItem} key={index}>
                    
                    <div className={styles.commentsValue}>{commentObj.comment}</div>
                    <div className={styles.commentsText}>"{commentObj.text}"</div>
                  </li>
                ))}
              </ul>
            </div>
          );
        }
        return null;
      };


      if(next){
        return <First selectedWordsArray={comments} userid={userid} />
      }
  
    return (
      <>
        <div className={styles.text} onClick={handleTextClick}>{text}</div>
        {renderSelectedText()}
        {startPos !== -1 && endPos !== -1 && (
          <Tooltip
            comment={tooltipComment}
            onChange={handleTooltipChange}
            onSave={() => {
              const commentObj = { text: text.slice(startPos, endPos), comment: tooltipComment };
              setComments([...comments, commentObj]);
              setTooltipComment("");
              setStartPos(-1);
              setEndPos(-1);
            }
          }
          onCancel={() => {
            setTooltipComment("");
              setStartPos(-1);
              setEndPos(-1);
          }}
          />
        )}
        {renderComments()}
        <Button onClick={() => setNext(!next)} color="#5C47C2" title="Ιεραρχηση αξιων" />
      </>
    );
  };
  
  const Tooltip = ({ comment, onChange, onSave, onCancel }) => {
    return (
      <div className={styles.tooltip}>
        <textarea className={styles.tooltipTextarea} value={comment} onChange={onChange} />
        <div className={styles.btnContainer}>
          <button className={styles.tooltipBtn} onClick={onSave}>Προσθήκη Αξίας</button>
          <button className={styles.tooltipCancelBtn} onClick={onCancel}>Ακύρωση</button>
        </div>
        
      </div>
    );
  };


export default TextAnnotations;
