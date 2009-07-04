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

(def eval (lambda (expr binds)
            (cond
             ((atom expr) (assoc expr binds))
             ((atom (car expr))
              (cond
               ((eq (car expr) (quote quote)) (cadr expr))
               ((eq (car expr) (quote atom))  (atom   (eval (cadr expr) binds)))
               ((eq (car expr) (quote eq))    (eq     (eval (cadr expr) binds)
                                                      (eval (caddr expr) binds)))
               ((eq (car expr) (quote car))   (car    (eval (cadr expr) binds)))
               ((eq (car expr) (quote cdr))   (cdr    (eval (cadr expr) binds)))
               ((eq (car expr) (quote cons))  (cons   (eval (cadr expr) binds)
                                                      (eval (caddr expr) binds)))
               ((eq (car expr) (quote cond))  (eval-cond (cdr expr) binds))
               (t (eval (cons (assoc (car expr) binds)
                              (cdr expr))
                        binds))))
             ((eq (caar expr) (quote def))
              (eval (cons (caddar expr) (cdr expr))
                    (cons (list (cadar expr) (car expr)) binds)))
             ((eq (caar expr) (quote lambda))
              (eval (caddar expr)
                    (append (pair (cadar expr) (eval-args (cdr expr) binds))
                            binds)))
             (t (assoc expr binds)))))

(def eval-cond (lambda (eval-cond_c eval-cond_a)
                 (cond ((eval (caar eval-cond_c) eval-cond_a)
                        (eval (cadar eval-cond_c) eval-cond_a))
                       (t (eval-cond (cdr eval-cond_c) eval-cond_a)))))

(def eval-args (lambda (eval-args_m eval-args_a)
                 (cond ((null eval-args_m) nil)
                       (t (cons (eval  (car eval-args_m) eval-args_a)
                                (eval-args (cdr eval-args_m) eval-args_a))))))

(def apply (lambda (apply_name apply_args)
             ((list apply_name (list (quote quote) apply_args)))))

