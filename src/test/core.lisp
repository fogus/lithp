(def and (lambda (x y)
           (cond (x
                  (cond (y t)
                        (t nil)))
                 (t nil))))

(def not (lambda (x)
           (cond (x nil)
                 (t t))))

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
            (and x (not y)) 
            (and (not x) y))))

(def xr (lambda (x y)
          (nand
           (nand x (nand x y))
           (nand y (nand x y)))))

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


