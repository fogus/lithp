(def mapcar (lambda (f lst)
              (cond
               ((null lst) (quote ())
                (t (cons
                    (f (car lst))
                    (mapcar f (cdr lst))))))))


(def null (lambda (x)
              (eq x (quote ()))))

(def reduce (lambda (f lst)
              (cond
               ((null lst) (f))
               (t (f (car lst)
                     (reduce f (cdr lst)))))))

