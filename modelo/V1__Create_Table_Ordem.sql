CREATE TABLE `ordem` (
  `id` INT(10) AUTO_INCREMENT PRIMARY KEY,
  `tipo_transacao` enum('COMPRA','VENDA') NOT NULL,
  `nome_ativo` enum('VIBRANIUM') NOT NULL,
  `valor_ordem` decimal(65,2) NOT NULL,
  `qtd_ordem` INT(10) NOT NULL,
  `preco_medio` decimal(65,2) NOT NULL,
  `data_ordem` datetime(6) NOT NULL,
  `status_ordem` enum('EFETIVADA','PROCESSANDO', 'CANCELADA', 'PENDENTE') NOT NULL,  
  `id_wallet` INT(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
