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

(def list (lambda (x y)
            (cons x (cons y (quote ())))))

(def pair (lambda (x y)
            (cond ((and (null x) (null y)) nil)
                  ((and (not (atom x)) (not (atom y)))
                   (cons (list (car x) (car y))
                         (pair (cdr x) (cdr y)))))))

(def assoc (lambda (x y)
             (cond ((eq (car (car y)) x) (car (cdr (car y))))
                   (t (assoc x (cdr y))))))

(def caar (lambda (x) (car (car x))))
(def cadr (lambda (x) (car (cdr x))))
(def caddr (lambda (x) (car (cdr (cdr x)))))
(def cadar (lambda (x) (car (cdr (car x)))))
(def caddar (lambda (x) (car (cdr (cdr (car x))))))

(def null (lambda (null_x)
            (eq null_x nil)))

(def mapcar (lambda (mapcar_f mapcar_lst)
              (cond
               ((null mapcar_lst) mapcar_lst)
               (t (cons
                   (mapcar_f (car mapcar_lst))
                   (mapcar mapcar_f (cdr mapcar_lst)))))))

(def reduce (lambda (reduce_f reduce_lst)
              (cond
               ((null reduce_lst) (reduce_f))
               (t (reduce_f (car reduce_lst)
                            (reduce reduce_f (cdr reduce_lst)))))))

(def append (lambda (append_x append_y)
              (cond ((null append_x) append_y)
                    (t (cons (car append_x) 
                             (append (cdr append_x) append_y))))))

(def filter (lambda (filter_f filter_lst)
              (cond
               ((null filter_lst) filter_lst)
               (t (cond
                   ((filter_f (car filter_lst)) (append 
                                                 (car filter_lst) 
                                                 (filter filter_f (cdr filter_lst))))
                   (t (filter filter_f (cdr filter_lst))))))))

(def eval (lambda (e a)
            (print e " " a)
            (cond
             ((atom e) (assoc e a))
             ((atom (car e))
              (cond
               ((eq (car e) (quote quote)) (cadr e))
               ((eq (car e) (quote atom))  (atom   (eval (cadr e) a)))
               ((eq (car e) (quote eq))    (eq     (eval (cadr e) a)
                                                   (eval (caddr e) a)))
               ((eq (car e) (quote car))   (car    (eval (cadr e) a)))
               ((eq (car e) (quote cdr))   (cdr    (eval (cadr e) a)))
               ((eq (car e) (quote cons))  (cons   (eval (cadr e) a)
                                                   (eval (caddr e) a)))
               ((eq (car e) (quote cond))  (evcon (cdr e) a))
               (t (eval (cons (assoc (car e) a)
                              (cdr e))
                        a))))
             ((eq (caar e) (quote def))
              (eval (cons (caddar e) (cdr e))
                    (cons (list (cadar e) (car e)) a)))
             ((eq (caar e) (quote lambda))
              (eval (caddar e)
                    (append (pair (cadar e) (evlis (cdr e) a))
                            a)))
             (t (assoc e a)))))

(def evcon (lambda (evcon_c evcon_a)
             (cond ((eval (caar evcon_c) evcon_a)
                    (eval (cadar evcon_c) evcon_a))
                   (t (evcon (cdr evcon_c) evcon_a)))))

(def evlis (lambda (evlis_m evlis_a)
             (cond ((null evlis_m) nil)
                   (t (cons (eval  (car evlis_m) evlis_a)
                            (evlis (cdr evlis_m) evlis_a))))))

(def apply (lambda (apply_name apply_args)
             ((list apply_name (list (quote quote) apply_args)))))
