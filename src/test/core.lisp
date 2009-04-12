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

(def append (lambda (x y)
                (cond ((null x) y)
                      (t (cons (car x) (append (cdr x) y))))))

(def filter (lambda (f lst)
              (cond
               ((null lst) lst)
               (t (cond
                   ((f (car lst)) (append (car lst) (filter f (cdr lst))))
                   (t (filter f (cdr lst))))))))

(def and (lambda (x y)
             (cond (x
                    (cond (y (quote t))
                          (t (quote ()))))
                   (t (quote ())))))

(def not (lambda (x)
             (cond (x (quote ()))
                   (t (quote t)))))

