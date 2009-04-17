(def and (lambda (and_x and_y)
           (cond (and_x
                  (cond (and_y t)
                        (t nil)))
                 (t nil))))

(def not (lambda (not_x)
           (cond (not_x nil)
                 (t t))))

(def nand (lambda (nand_x nand_y)
            (not (and nand_x nand_y))))

(def or (lambda (or_x or_y)
          (nand
           (nand or_x or_x)
           (nand or_y or_y))))

(def nor (lambda (nor_x nor_y)
           (not (or nor_x nor_y))))

(def xor (lambda (xor_x xor_y)
           (or
            (and xor_x (not xor_y))
            (and (not xor_x) xor_y))))

(def and_ (lambda (x y) (cond (x (cond (y t) (t nil))) (t nil))))
(def not_ (lambda (x) (cond (x nil) (t t))))
(def nand_ (lambda (x y) (not_ (and_ x y))))
(def or_ (lambda (x y) (nand_ (nand_ x x) (nand_ y y))))
(def xor_ (lambda (x y) (or_ (and_ x (not_ y)) (and_ (not_ x) y))))

(def mapcar (lambda (mapcar_f mapcar_lst)
              (cond
               ((null mapcar_lst) nil)
                (t (cons
                    (mapcar_f (car mapcar_lst))
                    (mapcar mapcar_f (cdr mapcar_lst))))))))


(def null (lambda (null_x)
              (eq null_x nil)))

(def reduce (lambda (reduce_f reduce_lst)
              (cond
               ((null reduce_lst) (reduce_f))
               (t (reduce_f (car reduce_lst)
                            (reduce reduce_f (cdr reduce_lst)))))))

(def append (lambda (x y)
                (cond ((null x) y)
                      (t (cons (car x) (append (cdr x) y))))))

(def filter (lambda (f lst)
              (cond
               ((null lst) lst)
               (t (cond
                   ((f (car lst)) (append (car lst) (filter f (cdr lst))))
                   (t (filter f (cdr lst))))))))


