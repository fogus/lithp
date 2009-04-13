(def and (lambda (x y)
             (cond (x
                    (cond (y (quote t))
                          (t (quote ()))))
                   (t (quote ())))))

(def not (lambda (x)
             (cond (x (quote ()))
                   (t (quote t)))))

(def nand (lambda (x y)
            (not (and x y))))

(def or (lambda (x y)
          (nand
           (nand x x) 
           (nand y y))))

(def nor (lambda (x y)
           (not (or x y))))

(def xor (lambda (x y)
           (or
            (and (not x) y)
            (and x (not y)))))

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


