1|#||4|164882|updatePanel|ctl00_ContentPlaceHolder1_updGlobal|
            <div id="ctl00_ContentPlaceHolder1_tab" class="tabPanel" style="width:100%;visibility:hidden;">
	<div id="ctl00_ContentPlaceHolder1_tab_header">
		<span id="ctl00_ContentPlaceHolder1_tab_tabGrid_tab"><span class="ajax__tab_outer"><span class="ajax__tab_inner"><span class="ajax__tab_tab" id="__tab_ctl00_ContentPlaceHolder1_tab_tabGrid">Contas a Receber</span></span></span></span><span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_tab"><span class="ajax__tab_outer"><span class="ajax__tab_inner"><span class="ajax__tab_tab" id="__tab_ctl00_ContentPlaceHolder1_tab_tabFiltro">Filtros  Avançados</span></span></span></span>
	</div><div id="ctl00_ContentPlaceHolder1_tab_body">
		<div id="ctl00_ContentPlaceHolder1_tab_tabGrid" class="ajax__tab_panel">
			
                        <script type="text/javascript">
                            function pageLoad() {
                                jQuery(document).ready(function () {
                                    /* filtros situação rápido e avançado*/
                                    var fieldsgroup1 = 'input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbPendentes, input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbQuitadas, input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbCanceladas, input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbNegativadas, input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbPendentesRapido, input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbQuitadasRapido, input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbCanceladasRapido, input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbNegativadasRapido';
                                    /* filtros vencidas negativadas rápido e avançado*/
                                    var fieldsgroup2 = 'input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbVencidas, input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbVencidasRapido';
                                    /* ao alterar situação rápido e avançado desmarcar vencidas e negativadas */
                                    jQuery(fieldsgroup1).change(function () {
                                        jQuery(fieldsgroup2).attr('checked', false);
                                    });

                                    /* ao alterar vencidas e negativadas desativar situação rápido e avançado */
                                    jQuery(fieldsgroup2).change(function () {
                                        jQuery(fieldsgroup1).attr('checked', false);
                                        /* se marcar vencidas demarcar negativadas */
                                        if (jQuery(this).attr('id') == 'ctl00_ContentPlaceHolder1_tab_tabGrid_cbVencidasRapido' || jQuery(this).attr('id') == 'ctl00_ContentPlaceHolder1_tab_tabFiltro_cbVencidas') {
                                            jQuery('input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbNegativadasRapido').attr('checked', false);
                                            if (jQuery('input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbNegativadas').is(':checked')) {
                                                /* trigger __doPostBack*/
                                                eval(jQuery('input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbNegativadas').attr('onclick'));
                                                jQuery('input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbNegativadas').attr('checked', false);
                                            }
                                        } else {
                                            /* se marcar desativadas desmarcar vencidas */
                                            jQuery('input#ctl00_ContentPlaceHolder1_tab_tabGrid_cbVencidasRapido').attr('checked', false);
                                            jQuery('input#ctl00_ContentPlaceHolder1_tab_tabFiltro_cbVencidas').attr('checked', false);
                                        }
                                    });
                                });
                            }

                            function filtroConceitoPearson() {
                                try {
                                    var situacao = $('#cmbConceitoPearson').val();
                                    let hdn = document.querySelector('#hdnConceitoPearson');
                                    hdn.value = situacao.join(",");
                                } catch (ex) {
                                    let hdn = document.querySelector('#hdnConceitoPearson');
                                    hdn.value = '';
                                }
                            }

                            function trataCmbConceitoPearson() {
                                if (document.getElementById('chkTodosConceitoPearson').checked) {
                                    let hdn = document.querySelector('#hdnTodosConceitosPearsonAux');
                                    let arrayVal = hdn.value.split(",");
                                    $('#cmbConceitoPearson').select2().val(arrayVal).trigger('change');
                                } else {
                                    $('#cmbConceitoPearson').select2().val([]).trigger('change');
                                }
                            }

                        </script>

                        <table width="100%" style="table-layout: fixed;">
                            <tr>
                                <td valign="top">
                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updGrid">
				
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_pnlGrid" style="border-width:1px;border-style:Solid;width:100%;overflow:auto;min-height: 550px;">
					
                                                <div id='ctl00_ContentPlaceHolder1_tab_tabGrid_grd_div'><img src='/WebResource.axd?d=QWsvX5INmtvAzTMjnUK8_SLLuPa4AUlUYjlcwVxtkEJWbXDL0wxCZ2lr7IFdl1yvvqcLLttwTup-BP2k0AWY0S_8ROvBWpGcxKldnyL9MxCArmJF4Ds5KcvC5Q6V9Q7F0&t=639244719340000000' alt='' title='' style='position:absolute;left:50%;top:50%;visibility:hidden;' /><div>
						<table class="grid" cellspacing="0" rules="all" tabindex="-1" onfocus="if (typeof(focusInsideGrid)==&#39;undefined&#39;) { focusInsideGrid = false;initializeGrid(this);} var te = this.getAttribute(&#39;tabExecuting&#39;); if(te &amp;&amp; te==&#39;1&#39;) return true;var ti = this.getAttribute(&#39;ti&#39;); this.rows[(ti ? ti : 1)].focus();" onkeydown="handleGridKeyPress(this,event,false);" border="1" id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd" style="width:3200px;border-collapse:collapse;">
							<tr class="gridHeader">
								<th scope="col" style="width:10px;"><input type='checkbox' hidefocus='true' style='cursor:pointer;' id='ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton' name='ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton'   onclick='CheckAll(this)'></th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'NumeroParcela|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Nº Parc.</a></th><th scope="col">Sacado</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'DataVencimento|1'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Data Ven.</a><img src='/WebResource.axd?d=blfWTeN7Bx-PZ-ttPC959I7bJzl0TboUzoZx-PELBFRn3f1ogLF_H8SKTjX6pDcf9imNoS4QOCMRIc51bz_BBL5XUYqt_RalDpIio9RsnySu0OEnPo_pEvXndRgCwJAX0&t=639244719340000000' alt='' title='' style='margin-left:5px;' /></th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'Valor|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Valor</a></th><th scope="col">Vlr. L&#237;quido</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'PlanoConta|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Categoria</a></th><th scope="col">Sit.</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'DataPagamento|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Data Pgto.</a></th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'ValorPago|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Valor Pago</a></th><th scope="col">Juros/Multa</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'FormaCobranca|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Forma de Cobrança</a></th><th scope="col">Tipo de Recebimento</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'Complemento|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Complemento</a></th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'NumeroBoleto|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Nº Boleto</a></th><th scope="col" style="width:150px;">Layout</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'SituacaoCNAB|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Situação CNAB</a></th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'NumeroRecibo|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Nº Recibo</a></th><th scope="col">N&#186; Contrato</th><th scope="col">N&#186; Cheque</th><th scope="col">Titular do Cheque</th><th scope="col">Banco</th><th scope="col">Ag&#234;ncia</th><th scope="col">Conta</th><th scope="col"><a class="gridHeader" href="#" onclick="$get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort').value = 'Empresa|0'; $get('ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort').click();">Empresa</a></th>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="84183|2|Maria Clara Reis Santana|14084|5|1|0|6|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl02_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl02_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl02$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl02_CheckBoxButton"> </label></span></td><td style="width:30px;">2</td><td onmouseover="showHint(&#39;hintAluno&#39;, 14084, false, event);" onmouseout="hideHint(false);" style="width:300px;">Maria Clara Reis Santana</td><td align="center" style="width:90px;">10/02/2025</td><td align="right" style="width:80px;">374.67</td><td align="right" style="width:80px;">374,67</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl02_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">04/11/2025</td><td align="right" style="width:80px;">374.67</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Cart&#227;o de D&#233;bito</td><td style="width:170px;">Cart&#227;o de D&#233;bito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl02_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;">4384</td><td align="left" style="width:100px;">3567/3</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="79399|8|Lucas Crynnsmam Ferreira dos Santos|17243|5|1|0|9|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl03_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl03_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl03$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl03_CheckBoxButton"> </label></span></td><td style="width:30px;">8</td><td onmouseover="showHint(&#39;hintAluno&#39;, 17243, false, event);" onmouseout="hideHint(false);" style="width:300px;">Lucas Crynnsmam Ferreira dos Santos</td><td align="center" style="width:90px;">25/08/2025</td><td align="right" style="width:80px;">336.78</td><td align="right" style="width:80px;">352,09</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl03_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">10/11/2025</td><td align="right" style="width:80px;">352.09</td><td align="right" style="width:80px;">15,31</td><td style="width:120px;">Cobran&#231;a Banc&#225;ria</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl03_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">4021/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80273|8|MARIA LUIZA SILVA DE SÁ|15723|5|1|0|10|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl04_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl04_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl04$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl04_CheckBoxButton"> </label></span></td><td style="width:30px;">8</td><td onmouseover="showHint(&#39;hintAluno&#39;, 15723, false, event);" onmouseout="hideHint(false);" style="width:300px;">MARIA LUIZA SILVA DE S&#193;</td><td align="center" style="width:90px;">05/09/2025</td><td align="right" style="width:80px;">415.10</td><td align="right" style="width:80px;">415,00</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl04_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">19/12/2025</td><td align="right" style="width:80px;">415.00</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl04_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">3645/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="79399|9|Lucas Crynnsmam Ferreira dos Santos|17243|5|1|0|9|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl05_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl05_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl05$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl05_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 17243, false, event);" onmouseout="hideHint(false);" style="width:300px;">Lucas Crynnsmam Ferreira dos Santos</td><td align="center" style="width:90px;">25/09/2025</td><td align="right" style="width:80px;">336.78</td><td align="right" style="width:80px;">351,60</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl05_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">09/12/2025</td><td align="right" style="width:80px;">351.60</td><td align="right" style="width:80px;">14,82</td><td style="width:120px;">Cobran&#231;a Banc&#225;ria</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl05_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">4021/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="82632|3|Carlos Ubiratan Evaristo De Souza Junior|13151|5|1|0|5|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl06_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl06_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl06$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl06_CheckBoxButton"> </label></span></td><td style="width:30px;">3</td><td onmouseover="showHint(&#39;hintAluno&#39;, 13151, false, event);" onmouseout="hideHint(false);" style="width:300px;">Carlos Ubiratan Evaristo De Souza Junior</td><td align="center" style="width:90px;">05/10/2025</td><td align="right" style="width:80px;">426.17</td><td align="right" style="width:80px;">439,24</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl06_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">06/11/2025</td><td align="right" style="width:80px;">439.24</td><td align="right" style="width:80px;">13,07</td><td style="width:120px;">Cart&#227;o de D&#233;bito</td><td style="width:170px;">Cart&#227;o de D&#233;bito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl06_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;">4417</td><td align="left" style="width:100px;">2405/2</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80273|9|MARIA LUIZA SILVA DE SÁ|15723|5|1|0|15|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl07_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl07_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl07$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl07_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 15723, false, event);" onmouseout="hideHint(false);" style="width:300px;">MARIA LUIZA SILVA DE S&#193;</td><td align="center" style="width:90px;">05/10/2025</td><td align="right" style="width:80px;">155.66</td><td align="right" style="width:80px;">155,66</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl07_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">02/02/2026</td><td align="right" style="width:80px;">155.66</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Cart&#227;o de Cr&#233;dito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl07_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">3645/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80455|9|Gabriel Esteves Santana|13511|5|1|0|14|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl08_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl08_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl08$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl08_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 13511, false, event);" onmouseout="hideHint(false);" style="width:300px;">Gabriel Esteves Santana</td><td align="center" style="width:90px;">10/10/2025</td><td align="right" style="width:80px;">435.85</td><td align="right" style="width:80px;">435,85</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl08_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">03/11/2025</td><td align="right" style="width:80px;">435.85</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Cart&#227;o de Cr&#233;dito</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl08_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">2833/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80924|9|AYALA  BARBOSA DO AMARAL|24115|5|1|0|11|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl09_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl09_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl09$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl09_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 24115, false, event);" onmouseout="hideHint(false);" style="width:300px;">AYALA  BARBOSA DO AMARAL</td><td align="center" style="width:90px;">25/10/2025</td><td align="right" style="width:80px;">395.33</td><td align="right" style="width:80px;">395,33</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl09_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">03/12/2025</td><td align="right" style="width:80px;">395.33</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl09_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">4963/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="79399|10|Lucas Crynnsmam Ferreira dos Santos|17243|5|1|0|9|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl10_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl10_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl10$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl10_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 17243, false, event);" onmouseout="hideHint(false);" style="width:300px;">Lucas Crynnsmam Ferreira dos Santos</td><td align="center" style="width:90px;">25/10/2025</td><td align="right" style="width:80px;">336.78</td><td align="right" style="width:80px;">351,47</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl10_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">29/12/2025</td><td align="right" style="width:80px;">351.47</td><td align="right" style="width:80px;">14,69</td><td style="width:120px;">Cobran&#231;a Banc&#225;ria</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl10_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">4021/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="82770|3|SOPHIA MENDES LENOIR DE ANDRADE|25827|5|1|0|5|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl11_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl11_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl11$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl11_CheckBoxButton"> </label></span></td><td style="width:30px;">3</td><td onmouseover="showHint(&#39;hintAluno&#39;, 25827, false, event);" onmouseout="hideHint(false);" style="width:300px;">SOPHIA MENDES LENOIR DE ANDRADE</td><td align="center" style="width:90px;">25/10/2025</td><td align="right" style="width:80px;">338.23</td><td align="right" style="width:80px;">346,00</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl11_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">05/11/2025</td><td align="right" style="width:80px;">346.00</td><td align="right" style="width:80px;">7,77</td><td style="width:120px;">Boleto</td><td style="width:170px;">Boleto</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl11_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">5262/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="79581|10|VALENTINA SOUZA THOME|19108|5|1|0|9|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl12_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl12_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl12$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl12_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 19108, false, event);" onmouseout="hideHint(false);" style="width:300px;">VALENTINA SOUZA THOME</td><td align="center" style="width:90px;">25/10/2025</td><td align="right" style="width:80px;">274.22</td><td align="right" style="width:80px;">282,44</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl12_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">24/11/2025</td><td align="right" style="width:80px;">282.44</td><td align="right" style="width:80px;">8,22</td><td style="width:120px;">Cobran&#231;a Banc&#225;ria</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl12_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">4469/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80887|9|Aghatta Moreira Ventin Lima|23996|5|1|0|4|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl13_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl13_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl13$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl13_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 23996, false, event);" onmouseout="hideHint(false);" style="width:300px;">Aghatta Moreira Ventin Lima</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">239.07</td><td align="right" style="width:80px;">245,84</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl13_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">24/11/2025</td><td align="right" style="width:80px;">245.84</td><td align="right" style="width:80px;">6,77</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Cart&#227;o de Cr&#233;dito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl13_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;">4546</td><td align="left" style="width:100px;">4948/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80083|10|ANA VICTÓRIA SANTANA DO ESPÍRITO SANTO|15281|5|1|0|12|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl14_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl14_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl14$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl14_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 15281, false, event);" onmouseout="hideHint(false);" style="width:300px;">ANA VICT&#211;RIA SANTANA DO ESP&#205;RITO SANTO</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">405.87</td><td align="right" style="width:80px;">405,87</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl14_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">03/11/2025</td><td align="right" style="width:80px;">405.87</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl14_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">3963/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="79318|10|CARLA TAMILLI BRAZ DE CERQUEIRA|23184|5|1|0|7|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl15_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl15_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl15$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl15_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 23184, false, event);" onmouseout="hideHint(false);" style="width:300px;">CARLA TAMILLI BRAZ DE CERQUEIRA</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">386.54</td><td align="right" style="width:80px;">400,00</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl15_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">18/12/2025</td><td align="right" style="width:80px;">400.00</td><td align="right" style="width:80px;">13,46</td><td style="width:120px;">Boleto</td><td style="width:170px;">Dinheiro</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl15_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;">4749</td><td align="left" style="width:100px;">4767/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80743|9|David Portinari Araujo De Santana|12353|5|1|0|5|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl16_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl16_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl16$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl16_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 12353, false, event);" onmouseout="hideHint(false);" style="width:300px;">David Portinari Araujo De Santana</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">398.50</td><td align="right" style="width:80px;">407,00</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl16_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">03/11/2025</td><td align="right" style="width:80px;">407.00</td><td align="right" style="width:80px;">8,50</td><td style="width:120px;">Cart&#227;o de Cr&#233;dito</td><td style="width:170px;">Cart&#227;o de Cr&#233;dito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl16_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;">4377</td><td align="left" style="width:100px;">1414/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80111|10|Isadora Da Cunha Paim|13413|5|1|0|10|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl17_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl17_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl17$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl17_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 13413, false, event);" onmouseout="hideHint(false);" style="width:300px;">Isadora Da Cunha Paim</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">409.52</td><td align="right" style="width:80px;">409,52</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl17_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">05/11/2025</td><td align="right" style="width:80px;">409.52</td><td align="right" style="width:80px;">0,00</td><td style="width:120px;">Cart&#227;o de Cr&#233;dito</td><td style="width:170px;">Cart&#227;o de Cr&#233;dito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl17_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">2713/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80029|10|Lívia Araújo Amorim|14118|5|1|0|16|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl18_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl18_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl18$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl18_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 14118, false, event);" onmouseout="hideHint(false);" style="width:300px;">L&#237;via Ara&#250;jo Amorim</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">404.86</td><td align="right" style="width:80px;">407,50</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl18_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">04/12/2025</td><td align="right" style="width:80px;">407.50</td><td align="right" style="width:80px;">2,64</td><td style="width:120px;">Boleto</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl18_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">3608/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="79873|10|Ludmila Bispo Santos Conceição|14174|5|1|0|10|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl19_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl19_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl19$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl19_CheckBoxButton"> </label></span></td><td style="width:30px;">10</td><td onmouseover="showHint(&#39;hintAluno&#39;, 14174, false, event);" onmouseout="hideHint(false);" style="width:300px;">Ludmila Bispo Santos Concei&#231;&#227;o</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">382.22</td><td align="right" style="width:80px;">397,21</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl19_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">19/12/2025</td><td align="right" style="width:80px;">397.21</td><td align="right" style="width:80px;">14,99</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl19_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">3675/2</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="83416|3|MARIANA GURGEL ROCHA|26080|5|1|0|6|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl20_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl20_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl20$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl20_CheckBoxButton"> </label></span></td><td style="width:30px;">3</td><td onmouseover="showHint(&#39;hintAluno&#39;, 26080, false, event);" onmouseout="hideHint(false);" style="width:300px;">MARIANA GURGEL ROCHA</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">374.25</td><td align="right" style="width:80px;">381,85</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl20_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">03/11/2025</td><td align="right" style="width:80px;">381.85</td><td align="right" style="width:80px;">7,60</td><td style="width:120px;">Boleto</td><td style="width:170px;">Boleto</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl20_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;"></td><td align="left" style="width:100px;">5311/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridAlternateRow" tabindex="0" onfocus="selectRow(this);" onblur="unselectRow(this);" keys="80886|9|Matheus Moreira Ventin Lima|23995|5|1|0|5|0|-100|0" onclick="ApplyStyle(document.getElementById(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl21_CheckBoxButton&#39;), &#39;gridSelectedRow&#39;, &#39;gridAlternateRow&#39;, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_HeaderButton&#39;)">
								<td style="width:10px;"><span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl21_CheckBoxButton" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl21$CheckBoxButton" onclick="unCheck(this);" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl21_CheckBoxButton"> </label></span></td><td style="width:30px;">9</td><td onmouseover="showHint(&#39;hintAluno&#39;, 23995, false, event);" onmouseout="hideHint(false);" style="width:300px;">Matheus Moreira Ventin Lima</td><td align="center" style="width:90px;">30/10/2025</td><td align="right" style="width:80px;">275.35</td><td align="right" style="width:80px;">283,15</td><td style="width:120px;">1. Mensalidades</td><td align="center" style="width:30px;">
                                                                <img id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl21_imgSituacao" title="Quitada" src="../images/quitada.gif" alt="1" style="border-width:0px;" />
                                                            </td><td align="center" style="width:80px;">24/11/2025</td><td align="right" style="width:80px;">283.15</td><td align="right" style="width:80px;">7,80</td><td style="width:120px;">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</td><td style="width:170px;">Cart&#227;o de Cr&#233;dito</td><td style="width:200px;">&nbsp;</td><td align="right" style="width:100px;"></td><td>
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl21_lblLayout" class="control-label" style="display:inline-block;width:150px;"></span>
                                                            </td><td style="width:120px;">&nbsp;</td><td align="right" style="width:100px;">4545</td><td align="left" style="width:100px;">4947/1</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:200px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td align="left" style="width:100px;">&nbsp;</td><td style="width:250px;">CCAA Paralela</td>
							</tr><tr class="gridFooter">
								<td colspan="37" style="width:10px;"><input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl22$ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort" id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_Sort" value="DataVencimento|0" /><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl22$ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort" value="" id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FireSort" class="btn btn-outline-secondary btn-sm btn-custom" CssImageClass="fa" CssTextClass="btn-sm" CssDisabledClass="btn btn-sm btn-outline-secondary disabled" aria-disabled="true" style="display:none;" /><input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl22$ctl00_ContentPlaceHolder1_tab_tabGrid_grd_PageIndex" id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_PageIndex" value="0" /><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl22$ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FirePageIndex" value="" id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FirePageIndex" class="btn btn-outline-secondary btn-sm btn-custom" CssImageClass="fa" CssTextClass="btn-sm" CssDisabledClass="btn btn-sm btn-outline-secondary disabled" aria-disabled="true" style="display:none;" /><span class="control-label">Página </span><select name="ctl00$ContentPlaceHolder1$tab$tabGrid$grd$ctl22$ctl00_ContentPlaceHolder1_tab_tabGrid_grd_cmb" id="ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_cmb" class="combo" combobox="false" onchange="$get(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_PageIndex&#39;).value = parseInt(this.value) - 1; $get(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_grd_ctl22_ctl00_ContentPlaceHolder1_tab_tabGrid_grd_FirePageIndex&#39;).click();" style="margin-bottom:0px;width:60px;">
									<option selected="selected" value="1">1</option>
									<option value="2">2</option>
									<option value="3">3</option>
									<option value="4">4</option>
									<option value="5">5</option>
									<option value="6">6</option>
									<option value="7">7</option>
									<option value="8">8</option>
									<option value="9">9</option>
									<option value="10">10</option>
									<option value="11">11</option>
									<option value="12">12</option>
									<option value="13">13</option>
									<option value="14">14</option>
									<option value="15">15</option>
									<option value="16">16</option>
									<option value="17">17</option>
									<option value="18">18</option>
									<option value="19">19</option>
									<option value="20">20</option>
									<option value="21">&gt; 20</option>

								</select><span class="control-label"> de 89 - 1770 registro(s)</span></td>
							</tr>
						</table>
					</div></div>
                                            
				</div>
                                            <input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$btnAtualizaGrid" value="" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnAtualizaGrid" class="btn btn-outline-secondary btn-sm btn-custom" CssImageClass="fa" CssTextClass="btn-sm" CssDisabledClass="btn btn-sm btn-outline-secondary disabled" aria-disabled="true" style="visibility: hidden;" />
                                        
			</div>
                                </td>
                                <td valign="top" style="width: 250px;">
                                    <div class="table_lateral">
                                        <div style="width: 95%" class="accordionHeaderSelected">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblAcoes" class="accordionHeaderSelected">Ações</span>
                                        </div>
                                        <div style="width: 95%" class="accordionContent">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updAbrir">
				
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divNovo" class="botaoAcao">
                                                        <a onclick="openWindow(1, &#39;cadconrec&#39;, &#39;Novo Plano&#39;,  &#39;ContaReceberCadastro.aspx&#39;, false, 610, 780, true, false, false, null);" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnNovo" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnNovo&#39;,&#39;&#39;)">Incluir</a>
                                                    </div>
                                                    <div class="botaoAcao">
                                                        <a onclick="editar();return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnEditar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnEditar&#39;,&#39;&#39;)">Editar</a>
                                                    </div>
                                                
			</div>
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updExcluir">
				
                                                    <div class="botaoAcao" >
                                                        <a onclick="if (! detalhes()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnDetalhes" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnDetalhes&#39;,&#39;&#39;)" style="width: 100%">Detalhes do Recebimento</a>
                                                    </div>
                                                    <div  Style="padding-bottom: 2px;">
                                                        <a onclick="if (! excluir()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnExcluir" class="btn btn-outline-danger" CssDisabledClass="btn btn-outline-danger disabled" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnExcluir&#39;,&#39;&#39;)" style="display:inline-block;width:100%;">Excluir</a>
                                                        <input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabGrid$hiddenID" id="ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID" />
                                                        <div class='divBackground' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos_background' style='display:none;z-index:2000;'></div><div tabindex='0' class='messageBox' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos' style='z-index:20001;display:none;' onkeypress='javascript:return WebForm_FireDefaultButton(event,"ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos_yesbutton")'><div class='divTitle'><span class='modal-dialog-title-text'>Atenção</span><span class='modal-dialog-title-close'></span></div><div class='divMessage'><div class='divMessage' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos_message'></div></div><div class='row divButton' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos_buttons'><div class='col text-left'>
                                        <button class='button btn custom-secondary btn-xs' style='margin: 5px; width: 90px;' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos_nobutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos');return false;">Não</button>
                                    </div><div class='col text-right'>
                            <button class='button btn btn-warning btn-messagebox btn-xs' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos_yesbutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaExcluirTransmitidos');return false;" focused='true'>
                                <i class='fa-solid fa-check' style='margin-right: 5px;'></i> Sim
                            </button>
                        </div></div></div>
                                                    </div>
                                                    <div class='divBackground' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas_background' style='display:none;z-index:2000;'></div><div tabindex='0' class='messageBox' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas' style='z-index:20001;display:none;' onkeypress='javascript:return WebForm_FireDefaultButton(event,"ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas_yesbutton")'><div class='divTitle'><span class='modal-dialog-title-text'>Atenção</span><span class='modal-dialog-title-close'></span></div><div class='divMessage'><div class='divMessage' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas_message'>Existe(m) título(s) transmitido(s) para processamento. Se cancelar, o(s) número(s) de boleto(s) da(s) parcela(s) será(ão) zerado(s). <br /> Confirma o cancelamento?</div></div><div class='row divButton' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas_buttons'><div class='col text-left'>
                                        <button class='button btn custom-secondary btn-xs' style='margin: 5px; width: 90px;' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas_nobutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas');return false;">Não</button>
                                    </div><div class='col text-right'>
                            <button class='button btn btn-warning btn-messagebox btn-xs' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas_yesbutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaCancelarParcelas');return false;" focused='true'>
                                <i class='fa-solid fa-check' style='margin-right: 5px;'></i> Sim
                            </button>
                        </div></div></div>
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_pnlDetalhes" style="background-color:White;height:315px;width:900px;display: none; border-radius: 12px;">
					
                                                        <div class="card">
                                                            <div class="card-header" id="hTitulo">
                                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_Label1" class="control-label">Detalhes do Recebimento:</span>
                                                            </div>
                                                            <div class="card-body">
                                                                <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_Panel8" style="border-width:1px;border-style:Solid;height:190px;width:100%;overflow:auto;">
						
                                                                    <div id='ctl00_ContentPlaceHolder1_tab_tabGrid_grdRecebimentos_div'><img src='/WebResource.axd?d=72ruhuVjuWyzCFU9dnUMgFRv5_LNSMUR3cVwOV0gr4G_t6Sx8U-LNS0Nby6lMekP01skvapK5UaCorQAUAmuuUVUld9zoXq80uLqDflr2zM1&t=639244719340000000' alt='' title='' style='position:absolute;left:50%;top:50%;visibility:hidden;' /><div>

						</div></div>
                                                                
					</div>
                                                            </div>
                                                        </div>

                                                        <br />
                                                        <div style="clear: both; width: 100%; display: table;">
                                                            <div style="float: right;margin-right: 10px;">
                                                                <div id='ctl00_ContentPlaceHolder1_tab_tabGrid_btnFecharDetalhes_div' tabindex="0" class='btn btn-sm btn-outline-danger' style="min-width:80px;width:90px;" onclick="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;hidePopup('mpeDetalhesBehaviorID'); $get('ctl00_ContentPlaceHolder1_tab_tabGrid_pnlDetalhes').style.display = 'none'; return false;" onkeydown="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;if ((event.which || event.keyCode) && (event.keyCode == 13 || event.keyCode == 32)){event.returnValue=false;event.cancel = true;clickButton(this);}" onmousedown="javascript:this.getElementsByTagName('div')[0].style.marginTop = '2px';this.getElementsByTagName('div')[0].style.marginLeft = '2px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseover="javascript:this.className='btn btn-sm btn-outline-danger btn btn-sm btn-outline-danger_hover';" onmouseup="javascript:this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseout="javascript:this.className='btn btn-sm btn-outline-danger';this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;"><div class='div_name_text' style='margin-top:0px; margin-left:0px;width:90px;'><center><div style="float: left;" class='fa fa-times topimg'></div><span class ='btn btn-sm btn-outline-danger_text'> Fechar </span></center></div>
</div><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$btnFecharDetalhes" value="Fechar" onclick="hidePopup(&#39;mpeDetalhesBehaviorID&#39;); $get(&#39;ctl00_ContentPlaceHolder1_tab_tabGrid_pnlDetalhes&#39;).style.display = &#39;none&#39;; return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnFecharDetalhes" class="btn btn-sm btn-outline-danger" aria-disabled="true" style="width:90px;display:none;" />
                                                            </div>
                                                        </div>
                                                    
				</div>
                                                    <a id="ctl00_ContentPlaceHolder1_tab_tabGrid_LinkButton2" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$LinkButton2&#39;,&#39;&#39;)" style="display: none">...</a>
                                                    
                                                
			</div>
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updQuitar">
				
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divQuitar" class="botaoAcao">
                                                        <a onclick="if (! quitar()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnQuitar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnQuitar&#39;,&#39;&#39;)">Quitar</a>
                                                        <input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabGrid$hdfFormaQuitar" id="ctl00_ContentPlaceHolder1_tab_tabGrid_hdfFormaQuitar" value="1" />
                                                    </div>
                                                    <div class='divBackground' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar_background' style='display:none;z-index:2000;'></div><div tabindex='0' class='messageBox' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar' style='z-index:20001;display:none;' onkeypress='javascript:return WebForm_FireDefaultButton(event,"ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar_yesbutton")'><div class='divTitle'><span class='modal-dialog-title-text'>Atenção</span><span class='modal-dialog-title-close'></span></div><div class='divMessage'><div class='divMessage' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar_message'>Existem parcelas anteriores desse aluno/cliente em aberto.<br />Tem certeza que deseja quitar esta parcela?</div></div><div class='row divButton' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar_buttons'><div class='col text-left'>
                                        <button class='button btn custom-secondary btn-xs' style='margin: 5px; width: 90px;' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar_nobutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar');return false;">Não</button>
                                    </div><div class='col text-right'>
                            <button class='button btn btn-warning btn-messagebox btn-xs' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar_yesbutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgPerguntaQuitar');return false;" focused='true'>
                                <i class='fa-solid fa-check' style='margin-right: 5px;'></i> Sim
                            </button>
                        </div></div></div>
                                                          <div class="modal fade" tabindex="-1" role="dialog" id="ModalProcessamento">
                                                            <div class="modal-dialog modal-md" role="document" style="top: 20%">
                                                                <div class="modal-content" style="border-radius: 10px; padding: 24px; box-shadow: 0px 4px 20px rgba(0,0,0,0.2); background-color: #fff;">
                                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_UpdateModalProcessamento">
					
                                                                            <div class="text-center">
                                                                                <h4 style="font-weight: 600; margin-bottom: 20px; color: #333;">Atenção</h4>
                                                                            </div>
                                                                            <div class="modal-body text-center" style="font-size: 15px; color: #444;">
                                                                                <p id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblMensagemParcelas" style="line-height: 1.6; margin-bottom: 0;"></p>
                                                                            </div>
                                                                            <div class="modal-footer d-flex justify-content-center gap-3" style="border-top: none; padding-top: 20px;">
                                                                                <div style="float: left; margin-right: auto;">
                                                                                    <div id='ctl00_ContentPlaceHolder1_tab_tabGrid_btnParcelasProcessamentoOk_div' tabindex="0" class='btn btn-sm btn-outline-secondary btn-custom' style="" onclick="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;clickButton($get('ctl00_ContentPlaceHolder1_tab_tabGrid_btnParcelasProcessamentoOk'));" onkeydown="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;if ((event.which || event.keyCode) && (event.keyCode == 13 || event.keyCode == 32)){event.returnValue=false;event.cancel = true;clickButton(this);}" onmousedown="javascript:this.getElementsByTagName('div')[0].style.marginTop = '2px';this.getElementsByTagName('div')[0].style.marginLeft = '2px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseover="javascript:this.className='btn btn-sm btn-outline-secondary btn-custom btn btn-sm btn-outline-secondary btn-custom_hover';" onmouseup="javascript:this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseout="javascript:this.className='btn btn-sm btn-outline-secondary btn-custom';this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;"><div class='div_name_text' style='margin-top:0px; margin-left:0px;'><center><div style="float: left;" class='fa'></div><span class ='btn-sm'> Ok </span></center></div>
</div><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$btnParcelasProcessamentoOk" value="Ok" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnParcelasProcessamentoOk" class="btn btn-sm btn-outline-secondary btn-custom" aria-disabled="true" style="display:none;" />
                                                                                </div>
                                                                                <div style="float: right;">
                                                                                    <div id='ctl00_ContentPlaceHolder1_tab_tabGrid_btnParcelasProcessamentoAcessar_div' tabindex="0" class='btn btn-sm btn-outline-secondary btn-custom' style="" onclick="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;clickButton($get('ctl00_ContentPlaceHolder1_tab_tabGrid_btnParcelasProcessamentoAcessar'));" onkeydown="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;if ((event.which || event.keyCode) && (event.keyCode == 13 || event.keyCode == 32)){event.returnValue=false;event.cancel = true;clickButton(this);}" onmousedown="javascript:this.getElementsByTagName('div')[0].style.marginTop = '2px';this.getElementsByTagName('div')[0].style.marginLeft = '2px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseover="javascript:this.className='btn btn-sm btn-outline-secondary btn-custom btn btn-sm btn-outline-secondary btn-custom_hover';" onmouseup="javascript:this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseout="javascript:this.className='btn btn-sm btn-outline-secondary btn-custom';this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;"><div class='div_name_text' style='margin-top:0px; margin-left:0px;'><center><div style="float: left;" class='fa'></div><span class ='btn-sm'>  </span></center></div>
</div><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$btnParcelasProcessamentoAcessar" value="" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnParcelasProcessamentoAcessar" class="btn btn-sm btn-outline-secondary btn-custom" aria-disabled="true" style="display:none;" />
                                                                                </div>
                                                                            </div>
                                                                        
				</div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                
			</div>
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updRecibo">
				
                                                    <div class='divBackground' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo_background' style='display:none;z-index:2000;'></div><div tabindex='0' class='messageBox' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo' style='z-index:20001;display:none;' onkeypress='javascript:return WebForm_FireDefaultButton(event,"ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo_yesbutton")'><div class='divTitle'><span class='modal-dialog-title-text'>Atenção</span><span class='modal-dialog-title-close'></span></div><div class='divMessage'><div class='divMessage' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo_message'>Este recibo não suporta a impressão de mais de cinco parcelas. <br/><br/> Deseja imprimir o recibo em duas vias?</div></div><div class='row divButton' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo_buttons'><div class='col text-left'>
                                        <button class='button btn custom-secondary btn-xs' style='margin: 5px; width: 90px;' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo_nobutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo');return false;">Não</button>
                                    </div><div class='col text-right'>
                            <button class='button btn btn-warning btn-messagebox btn-xs' id='ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo_yesbutton' onclick="SPMessageBox_close('ctl00_ContentPlaceHolder1_tab_tabGrid_msgRecibo');return false;" focused='true'>
                                <i class='fa-solid fa-check' style='margin-right: 5px;'></i> Sim
                            </button>
                        </div></div></div>
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divCancelar" class="botaoAcao">
                                                        <a onclick="if (! cancelar()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnCancelar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnCancelar&#39;,&#39;&#39;)">Cancelar</a>
                                                    </div>
                                                    <div class="botaoAcao">
                                                        <a onclick="if (! recibo()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnRecibo" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnRecibo&#39;,&#39;&#39;)">Imprimir Recibo</a>
                                                    </div>
                                                    
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divImprimirBoletos" class="botaoAcao">
                                                        <a onclick="if (! impBoletos()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnImprimirBoletos" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnImprimirBoletos&#39;,&#39;&#39;)">Imprimir Boletos</a>
                                                    </div>
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divRenegociacao" class="botaoAcao">
                                                        <a onclick="renegociacao();return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnRenegociacao" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnRenegociacao&#39;,&#39;&#39;)">Renegociar Parcelas</a>
                                                    </div>
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divNegativar" class="botaoAcao">
                                                        <a onclick="if (! negativar()) return false;" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnNegativar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$btnNegativar&#39;,&#39;&#39;)">Negativar Parcelas</a>
                                                    </div>
                                                
			</div>
                                        </div>
                                        <br />
                                        <div style="width: 95%" class="accordionHeaderSelected">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblFiltrosRapidos" class="accordionHeaderSelected">Filtros Rápidos</span>
                                        </div>
                                        <div style="width: 95%" class="accordionContent">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updFiltroRapido">
				
                                                    <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_pnlFiltroRapido" onkeypress="javascript:return WebForm_FireDefaultButton(event, &#39;ctl00_ContentPlaceHolder1_tab_tabGrid_btnFiltroRapido&#39;)">
					
                                                        <div style="clear: both; width: 100%">
                                                            <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_Panel4">
						<fieldset>
							<legend>
								Situação
							</legend>
                                                                <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_cbPendentesRapido" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$cbPendentesRapido" checked="checked" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_cbPendentesRapido">Pendentes</label></span>
                                                                <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_cbQuitadasRapido" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$cbQuitadasRapido" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_cbQuitadasRapido">Quitadas</label></span>
                                                                <br />
                                                                <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_cbCanceladasRapido" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$cbCanceladasRapido" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_cbCanceladasRapido">Canceladas</label></span>
                                                                <br />
                                                                <br />
                                                                <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_Panel6">
								<fieldset>
									<legend>
										Pendentes
									</legend>
                                                                    <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_cbVencidasRapido" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$cbVencidasRapido" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_cbVencidasRapido">Vencidas</label></span>
                                                                    <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_cbNegativadasRapido" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$cbNegativadasRapido" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_cbNegativadasRapido">Negativadas</label></span>
                                                                
								</fieldset>
							</div>
                                                            
						</fieldset>
					</div>
                                                        </div>
                                                        <div style="clear: both; width: 100%">
                                                            <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_Label2" class="control-label">Vencimento:</span>
                                                            <br />
                                                            <select name="ctl00$ContentPlaceHolder1$tab$tabGrid$cmbVencimento" id="ctl00_ContentPlaceHolder1_tab_tabGrid_cmbVencimento" class="combo" style="width:99%;">
						<option value="0">(Todos)</option>
						<option value="1">Janeiro</option>
						<option value="2">Fevereiro</option>
						<option value="3">Mar&#231;o</option>
						<option value="4">Abril</option>
						<option value="5">Maio</option>
						<option value="6">Junho</option>
						<option value="7">Julho</option>
						<option value="8">Agosto</option>
						<option selected="selected" value="9">Setembro</option>
						<option value="10">Outubro</option>
						<option value="11">Novembro</option>
						<option value="12">Dezembro</option>

					</select>
                                                        </div>
                                                        <div style="clear: both; width: 100%; margin-top: 10px;">
                                                            <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabGrid_chkFiltrarAnoAtual" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabGrid$chkFiltrarAnoAtual" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$chkFiltrarAnoAtual\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabGrid_chkFiltrarAnoAtual">Filtrar pelo ano atual</label></span>
                                                        </div>
                                                        <div style="clear: both; width: 100%">
                                                            <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_Label20" class="control-label">Vencimento entre:</span>
                                                            <br />
                                                            <div style="margin-bottom: 5px;">
                                                                
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />

<input name="ctl00$ContentPlaceHolder1$tab$tabGrid$wcdVencimentoRapidoInicial$txtData" type="text" id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_txtData" class="form-control input-sm" data-calendario="true" style="width:85px;" />
<a id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_btnCalendar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$wcdVencimentoRapidoInicial$btnCalendar&#39;,&#39;&#39;)"><i id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_image1" class="fa fa-calendar-days CorMenuItem" alt="V" style="cursor: pointer; font-size: 16px; margin-left: 5px;"></i></a>
<input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabGrid$wcdVencimentoRapidoInicial$mask_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_mask_ClientState" />


                                                            </div>
                                                            <div>
                                                                
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />

<input name="ctl00$ContentPlaceHolder1$tab$tabGrid$wcdVencimentoRapidoFinal$txtData" type="text" id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_txtData" class="form-control input-sm" data-calendario="true" style="width:85px;" />
<a id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_btnCalendar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabGrid$wcdVencimentoRapidoFinal$btnCalendar&#39;,&#39;&#39;)"><i id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_image1" class="fa fa-calendar-days CorMenuItem" alt="V" style="cursor: pointer; font-size: 16px; margin-left: 5px;"></i></a>
<input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabGrid$wcdVencimentoRapidoFinal$mask_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_mask_ClientState" />


                                                            </div>
                                                        </div>
                                                        <br />
                                                        <div style="clear: both; width: 100%">
                                                            <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_Label11" class="control-label">Sacado/Nº Carnê</span>
                                                            <br />
                                                            <input name="ctl00$ContentPlaceHolder1$tab$tabGrid$txtSacado" type="text" id="ctl00_ContentPlaceHolder1_tab_tabGrid_txtSacado" class="form-control input-sm" style="width:99%;" />
                                                        </div>
                                                        <br />
                                                        <div style="clear: both; width: 100%; display: table;">
                                                            <div style="float: right;">
                                                                <div id='ctl00_ContentPlaceHolder1_tab_tabGrid_btnFiltroRapido_div' tabindex="0" class='btn btn-outline-primary' style="" onclick="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;clickButton($get('ctl00_ContentPlaceHolder1_tab_tabGrid_btnFiltroRapido'));" onkeydown="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;if ((event.which || event.keyCode) && (event.keyCode == 13 || event.keyCode == 32)){event.returnValue=false;event.cancel = true;clickButton(this);}" onmousedown="javascript:this.getElementsByTagName('div')[0].style.marginTop = '2px';this.getElementsByTagName('div')[0].style.marginLeft = '2px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseover="javascript:this.className='btn btn-outline-primary btn btn-outline-primary_hover';" onmouseup="javascript:this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseout="javascript:this.className='btn btn-outline-primary';this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;"><div class='div_name_text' style='margin-top:0px; margin-left:0px;'><center><div style="float: left;" class='fa fa-search topimg'></div><span class ='btn btn-outline-primary_text'> Filtrar </span></center></div>
</div><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabGrid$btnFiltroRapido" value="Filtrar" id="ctl00_ContentPlaceHolder1_tab_tabGrid_btnFiltroRapido" class="btn btn-outline-primary" style="display:none;" />
                                                            </div>
                                                        </div>
                                                    
				</div>
                                                
			</div>
                                        </div>
                                        <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_pnlResumos">
				
                                            <br />
                                            <div style="width: 95%" class="accordionHeaderSelected">
                                                <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblResumos" class="accordionHeaderSelected">Resumos</span>
                                            </div>
                                            <div style="width: 95%" class="accordionContent">
                                                <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_updResumo">
					
                                                        
                                                        <div id="ctl00_ContentPlaceHolder1_tab_tabGrid_divTotalPagas">
                                                            <span id="ctl00_ContentPlaceHolder1_tab_tabGrid_lblTotalPagas" class="control-label" style="color: Green; margin-left: 8px;">Recebidas:  R$ 669.386,65</span>
                                                            <br />
                                                        </div>
                                                        
                                                    
				</div>
                                            </div>
                                        
			</div>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    
		</div><div id="ctl00_ContentPlaceHolder1_tab_tabFiltro" class="ajax__tab_panel" style="display:none;visibility:hidden;">
			
                        <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_updAC">
				<input type="button" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$acSacadoDummyButtonSelected" value="" onclick="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$acSacadoDummyButtonSelected&#39;,&#39;&#39;)" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_acSacadoDummyButtonSelected" class="btn btn-outline-secondary btn-sm btn-custom" CssImageClass="fa" CssTextClass="btn-sm" CssDisabledClass="btn btn-sm btn-outline-secondary disabled" aria-disabled="true" style="display:none;visibility:hidden;" /><input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$acSacadoDummyButtonSelectedHiddenField" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_acSacadoDummyButtonSelectedHiddenField" /><input type="button" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$acResponsavelDummyButtonSelected" value="" onclick="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$acResponsavelDummyButtonSelected&#39;,&#39;&#39;)" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_acResponsavelDummyButtonSelected" class="btn btn-outline-secondary btn-sm btn-custom" CssImageClass="fa" CssTextClass="btn-sm" CssDisabledClass="btn btn-sm btn-outline-secondary disabled" aria-disabled="true" style="display:none;visibility:hidden;" /><input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$acResponsavelDummyButtonSelectedHiddenField" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_acResponsavelDummyButtonSelectedHiddenField" />
			</div>
                        <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_updFiltro">
				
                                <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel1" onkeypress="javascript:return WebForm_FireDefaultButton(event, &#39;ctl00_ContentPlaceHolder1_tab_tabFiltro_btnFiltrar&#39;)">
					
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <table id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado" border="0">
						<tr>
							<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado_0" type="radio" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$rblSacado" value="1" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$rblSacado$0\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado_0">Aluno</label></span></td><td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado_1" type="radio" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$rblSacado" value="2" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$rblSacado$1\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado_1">Cliente</label></span></td><td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado_2" type="radio" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$rblSacado" value="0" checked="checked" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblSacado_2">Ambos</label></span></td>
						</tr>
					</table>
                                            
                                        </div>
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <table id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblResponsavel" border="0">
						<tr>
							<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblResponsavel_0" type="radio" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$rblResponsavel" value="1" checked="checked" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblResponsavel_0">Responsável</label></span></td><td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblResponsavel_1" type="radio" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$rblResponsavel" value="2" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$rblResponsavel$1\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_rblResponsavel_1">Empresa</label></span></td>
						</tr>
					</table>
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_acResponsavel" class="autoComplete" style="display:inline-block;width:250px;"><input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$acResponsavel$acResponsavelTextBox" type="text" autocomplete="off" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_acResponsavel_acResponsavelTextBox" key="" autocomplete="off" dataSrc="acResponsavel" tabindex="0" class="textBox wickEnabled:MYCUSTOMFLOATER" btnSelected="ctl00_ContentPlaceHolder1_tab_tabFiltro_acResponsavelDummyButtonSelected" onblur="if(eval(&#39;loading&#39; + dataSrc) == true){ this.focus(); this.select(); }" style="width:250px;" /></span>
                                        </div>
                                        <div style="float: left; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_lblTurma" class="control-label">Turma:</span>
                                            <br />
                                            <select name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cmbTurmas" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cmbTurmas" class="combo" style="width:200px;">
						<option selected="selected" value="0">(Selecione)</option>
						<option value="9607">11</option>
						<option value="9618">2/2026 - Baby Class - Baby 2.1</option>
						<option value="9148">2/2026 - English Course - English 10.1</option>
						<option value="9184">2/2026 - English Course - English 10.2</option>
						<option value="9409">2/2026 - English Course - English 11.30</option>
						<option value="9434">2/2026 - English Course - English 11.31</option>
						<option value="9160">2/2026 - English Course - English 4.1</option>
						<option value="9168">2/2026 - English Course - English 4.2</option>
						<option value="9188">2/2026 - English Course - English 4.3</option>
						<option value="9186">2/2026 - English Course - English 5.1</option>
						<option value="9146">2/2026 - English Course - English 6.1</option>
						<option value="9174">2/2026 - English Course - English 6.2</option>
						<option value="9608">2/2026 - English Course - English 6.30</option>
						<option value="9162">2/2026 - English Course - English 7.1</option>
						<option value="9182">2/2026 - English Course - English 8.2</option>
						<option value="9633">2/2026 - English Course - English 8.20</option>
						<option value="9156">2/2026 - English Course - English 9.1</option>
						<option value="9164">2/2026 - English Course - English 9.2</option>
						<option value="9637">2/2026 - English Course - English 9.30</option>
						<option value="9621">2/2026 - English Course - English A1.1</option>
						<option value="9579">2/2026 - English Course - English A1.2</option>
						<option value="9330">2/2026 - English Course - English A2.1</option>
						<option value="9332">2/2026 - English Course - English A2.2</option>
						<option value="9456">2/2026 - English Course - English A2.20</option>
						<option value="9642">2/2026 - English Course - English A2.30</option>
						<option value="9158">2/2026 - English Course - English A3.1</option>
						<option value="9180">2/2026 - English Course - English A3.2</option>
						<option value="9652">2/2026 - English Course - English A3.30</option>
						<option value="9568">2/2026 - English Course - English T1.1</option>
						<option value="9639">2/2026 - English Course - English T1.21</option>
						<option value="9144">2/2026 - English Course - English T2.1</option>
						<option value="9172">2/2026 - English Course - English T3.1</option>
						<option value="9603">2/2026 - Espanhol - Espanhol 1.30</option>
						<option value="9385">2/2026 - Espanhol - Espanhol 2.30</option>
						<option value="9190">2/2026 - Kids Course - Kids 2.1</option>
						<option value="9152">2/2026 - Kids Course - Kids 4.1</option>
						<option value="9150">2/2026 - Kids Course - Kids 6.1</option>
						<option value="9178">2/2026 - Kids Course - Kids 8.1</option>
						<option value="9142">2/2026 - Preteens Course - Preteen 2.1</option>
						<option value="9176">2/2026 - Teacher&#180;s Course.1</option>
						<option value="9641">2/2026 - Teacher&#180;s Course.30</option>
						<option value="9653">2/2026 - VIP -  English A1</option>
						<option value="9351">2/2026 -BABY CLASS - BABY 6.1</option>
						<option value="9654">2/2026- English Course - English A1.30</option>
						<option value="9405">2026/1 English Course - English A VIP 1.1</option>

					</select>
                                        </div>
                                        
                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label16" class="control-label">CPF:</span>
                                            <br />
                                            <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtCPF" type="text" value="___.___.___-__" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtCPF" class="form-control input-sm" style="width:110px;" />
                                            <input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$maskCPF_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_maskCPF_ClientState" />
                                        </div>
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label13" class="control-label">Tipo de Bolsa:</span>
                                            <br />
                                            <select name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cmbTipoBolsa" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cmbTipoBolsa" class="combo" style="width:250px;">
						<option selected="selected" value="0">(Selecione)</option>
						<option value="225">25% Desconto -  Ex Aluno 2026.1.2</option>
						<option value="222">25% Desconto -  Ex Aluno 2026.1off</option>
						<option value="216">25% Desconto - Promo&#231;&#227;o Aluno Novo 2026.1</option>
						<option value="219">25% Desconto - Promo&#231;&#227;o Aluno Novo 2026.1.2</option>
						<option value="272">25% PROMO&#199;&#195;O 65 ANOS CCAA</option>
						<option value="253">25% Semana do Consumidor</option>
						<option value="226">28% Desconto -  Ex Aluno 2026.1.2</option>
						<option value="223">28% Desconto -  Ex Aluno 2026.1off</option>
						<option value="217">28% Desconto - Promo&#231;&#227;o Aluno Novo 2026.1</option>
						<option value="220">28% Desconto - Promo&#231;&#227;o Aluno Novo 2026.1.2</option>
						<option value="273">28% PROMO&#199;&#195;O 65 ANOS CCAA</option>
						<option value="254">28% Semana do Consumidor</option>
						<option value="227">30% Desconto -  Ex Aluno 2026.1.2</option>
						<option value="224">30% Desconto -  Ex Aluno 2026.1off</option>
						<option value="218">30% Desconto - Promo&#231;&#227;o Aluno Novo 2026.1</option>
						<option value="221">30% Desconto - Promo&#231;&#227;o Aluno Novo 2026.1.2</option>
						<option value="274">30% PROMO&#199;&#195;O 65 ANOS CCAA</option>
						<option value="255">30% Semana do Consumidor</option>
						<option value="127">Abono Estacionamento</option>
						<option value="56">Bolsa 100%</option>
						<option value="99">Desconto 10%</option>
						<option value="87">Desconto 15%</option>
						<option value="88">Desconto 17%</option>
						<option value="89">Desconto 20%</option>
						<option value="84">Desconto 25%</option>
						<option value="85">Desconto 28%</option>
						<option value="86">Desconto 30%</option>
						<option value="16">Desconto 40</option>
						<option value="8">Desconto 41</option>
						<option value="9">Desconto 42</option>
						<option value="10">Desconto 43</option>
						<option value="11">Desconto 44</option>
						<option value="7">Desconto 45</option>
						<option value="97">Desconto 45% Reprovados</option>
						<option value="12">Desconto 46</option>
						<option value="13">Desconto 47</option>
						<option value="14">Desconto 48</option>
						<option value="15">Desconto 49</option>
						<option value="2">Desconto Col&#244;nia 50</option>
						<option value="6">Desconto Conjunto</option>
						<option value="5">Desconto de Aluno  Antigos 40%</option>
						<option value="4">Desconto de Alunos Novos 40</option>
						<option value="96">Desconto VIP COURSE 5% a vista</option>
						<option value="107">Pagamento com&#160;CCAA$</option>
						<option value="279">PROMO&#199;&#195;O 65 ANOS CCAA</option>
						<option value="125">Toelf ITP - Aplica&#231;&#227;o em grupo</option>

					</select>
                                        </div>
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_lblDocumento" class="control-label">Documento:</span>
                                            <br />
                                            <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtDocumento" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtDocumento" class="form-control input-sm" style="width:200px;" />
                                        </div>

                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label3" class="control-label">Categoria:</span>
                                            <br />
                                            <select name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cmbPlanoConta" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cmbPlanoConta" class="combo" style="width:250px;">
						<option value="0|0">(Selecione)</option>
						<option value="-54|0">(Migra&#231;&#227;o)</option>
						<option selected="selected" value="-100|0">1. Mensalidades</option>
						<option value="-147|0">   • 1.1. Receita de mensalidades ingl&#234;s - 1&#186; F</option>
						<option value="-156|0">   • 1.10. Receita de mensalidades espanhol - 2&#186; R</option>
						<option value="-157|0">   • 1.11. Receita de mensalidades portugu&#234;s - 1&#186; F</option>
						<option value="-158|0">   • 1.12. Receita de mensalidades portugu&#234;s - 1&#186; R</option>
						<option value="-159|0">   • 1.13. Receita de mensalidades portugu&#234;s - 2&#186; F</option>
						<option value="-160|0">   • 1.14. Receita de mensalidades portugu&#234;s - 2&#186; R</option>
						<option value="-161|0">   • 1.15. Receita de mensalidades In-company - 1&#186; R</option>
						<option value="-162|0">   • 1.16. Receita de mensalidades In-company - 2&#186; R</option>
						<option value="-163|0">   • 1.17. Receita de juros e multa - mensalidades</option>
						<option value="-164|0">   • 1.18. Receita de troco - mensalidades</option>
						<option value="-165|0">   • 1.19. Receita mensalidades per&#237;odos anteriores</option>
						<option value="-148|0">   • 1.2. Receita de mensalidades ingl&#234;s - 1&#186; R</option>
						<option value="1001|0">   • 1.20. Receita de multa contratual</option>
						<option value="-149|0">   • 1.3. Receita de mensalidades ingl&#234;s - 2&#186; F</option>
						<option value="-150|0">   • 1.4. Receita de mensalidades ingl&#234;s - 2&#186; R</option>
						<option value="-151|0">   • 1.5. Receita de mensalidades ingl&#234;s - 3&#186; per&#237;odo</option>
						<option value="-152|0">   • 1.6. Receita de mensalidades ingl&#234;s - 4&#186; per&#237;odo</option>
						<option value="-153|0">   • 1.7. Receita de mensalidades espanhol - 1&#186; F</option>
						<option value="-154|0">   • 1.8. Receita de mensalidades espanhol - 1&#186; R</option>
						<option value="-155|0">   • 1.9. Receita de mensalidades espanhol - 2&#186; F</option>
						<option value="-101|0">10. Publicidade</option>
						<option value="-169|0">   • 10.4. Estorno de taxa de publicidade</option>
						<option value="-170|0">   • 10.5. Estorno de investimento local</option>
						<option value="-171|0">   • 10.6. Estorno - Outros</option>
						<option value="-103|0">11. Marketing</option>
						<option value="-181|0">   • 11.10. Estorno - Outros</option>
						<option value="-177|0">   • 11.6. Estorno de brindes</option>
						<option value="-178|0">   • 11.7. Estorno de uniformes</option>
						<option value="-179|0">   • 11.8. Estorno de eventos externos</option>
						<option value="-180|0">   • 11.9. Estorno de eventos internos</option>
						<option value="-105|0">12. Folha Equipe Administrativa</option>
						<option value="-191|0">   • 12.10. Estorno de sal&#225;rio - consultor de idiomas</option>
						<option value="-192|0">   • 12.11. Estorno de sal&#225;rio - agente de atendimento</option>
						<option value="-193|0">   • 12.12. Estorno de outros sal&#225;rios</option>
						<option value="-197|0">   • 12.16. Estorno de comiss&#227;o - consultor de idiomas</option>
						<option value="-198|0">   • 12.17. Estorno comiss&#227;o  agentes de atendimento</option>
						<option value="-199|0">   • 12.18. Estorno de comiss&#227;o - diretor</option>
						<option value="-188|0">   • 12.7. Estorno de sal&#225;rio - diretor</option>
						<option value="-189|0">   • 12.8. Estorno sal&#225;rio auxiliar servi&#231;os gerais</option>
						<option value="-190|0">   • 12.9. Estorno de sal&#225;rio - agente patrimonial</option>
						<option value="-107|0">13. Pr&#243;-labore</option>
						<option value="-201|0">   • 13.2. Estorno de pr&#243;-labore</option>
						<option value="-109|0">14. Encargos Administrativos</option>
						<option value="-211|0">   • 14.10. Estorno de hora extra administrativo</option>
						<option value="-212|0">   • 14.11. Estorno de vale-transporte administrativo</option>
						<option value="-213|0">   • 14.12. Estorno de vale-alimenta&#231;&#227;o administrativo</option>
						<option value="-214|0">   • 14.13. Estorno de plano de sa&#250;de administrativo</option>
						<option value="-215|0">   • 14.14. Estorno de f&#233;rias administrativo</option>
						<option value="-216|0">   • 14.15. Estorno de 13&#186; administrativo</option>
						<option value="-217|0">   • 14.16. Estorno de INSS empregador administrativo</option>
						<option value="-218|0">   • 14.17. Estorno de FGTS administrativo</option>
						<option value="-219|0">   • 14.18. Estorno de outros</option>
						<option value="-111|0">15. Despesas Operacionais</option>
						<option value="-237|0">   • 15.18. Estorno - Contador</option>
						<option value="-238|0">   • 15.19. Estorno - Advogado</option>
						<option value="-239|0">   • 15.20. Estorno de material de escrit&#243;rio</option>
						<option value="-240|0">   • 15.21. Estorno de material de limpeza</option>
						<option value="-241|0">   • 15.22. Estorno de despesas com transporte</option>
						<option value="-242|0">   • 15.23. Estorno de despesas eventuais</option>
						<option value="-243|0">   • 15.24. Estorno de despesas com c&#243;pias e impress&#245;es</option>
						<option value="-244|0">   • 15.25. Estorno de despesas com correios</option>
						<option value="-245|0">   • 15.26. Estorno de despesas com lanches e refei&#231;&#245;es</option>
						<option value="-246|0">   • 15.27. Estorno de combust&#237;veis e lubrificantes</option>
						<option value="-247|0">   • 15.28. Estorno de despesas de cobran&#231;a banc&#225;ria</option>
						<option value="-113|0">16. Despesa de Infraestrutura</option>
						<option value="-267|0">   • 16.20. Estorno - &#193;gua e esgoto</option>
						<option value="-268|0">   • 16.21. Estorno - Coleta de lixo</option>
						<option value="-269|0">   • 16.22. Estorno - G&#225;s</option>
						<option value="-270|0">   • 16.23. Estorno - Alarme</option>
						<option value="-271|0">   • 16.24. Estorno - TV por assinatura</option>
						<option value="-272|0">   • 16.25. Estorno - Assinaturas (jornais e revistas)</option>
						<option value="-273|0">   • 16.26. Estorno - Despesas manut  condicionador  ar</option>
						<option value="-274|0">   • 16.27. Estorno - Manuten&#231;&#245;es gerais</option>
						<option value="-275|0">   • 16.28. Estorno - Manuten&#231;&#227;o de equipamentos</option>
						<option value="-276|0">   • 16.29. Estorno - manut de computadores e sistemas</option>
						<option value="-277|0">   • 16.30. Estorno - Manuten&#231;&#227;o estrutural</option>
						<option value="-278|0">   • 16.31. Estorno - Investimentos</option>
						<option value="-279|0">   • 16.32. Estorno - Outros</option>
						<option value="-280|0">   • 16.33. Estorno - Aluguel</option>
						<option value="-281|0">   • 16.34. Estorno - Condom&#237;nio</option>
						<option value="-282|0">   • 16.35. Estorno - Energia</option>
						<option value="-283|0">   • 16.36. Estorno -  Telefone</option>
						<option value="-284|0">   • 16.37. Estorno - Internet</option>
						<option value="-285|0">   • 16.38. Estorno - Seguro</option>
						<option value="-115|0">17. Despesas com Impostos e Contribui&#231;&#245;es</option>
						<option value="-295|0">   • 17.10. Estorno - ISS</option>
						<option value="-296|0">   • 17.11. Estorno - PIS</option>
						<option value="-297|0">   • 17.12. Estorno - COFINS</option>
						<option value="-298|0">   • 17.13. Estorno - CSL</option>
						<option value="-299|0">   • 17.14. Estorno - Simples</option>
						<option value="-293|0">   • 17.8. Estorno - IPTU</option>
						<option value="-294|0">   • 17.9. Estorno - ICMS outros produtos</option>
						<option value="-117|0">18. Despesas com taxas </option>
						<option value="-309|0">   • 18.10. Estorno - Taxa de inc&#234;ndio</option>
						<option value="-310|0">   • 18.11. Estorno - Certificado do corpo de bombeiros</option>
						<option value="-311|0">   • 18.12. Estorno - Outros</option>
						<option value="-306|0">   • 18.7. Estorno - Taxas banc&#225;rias</option>
						<option value="-307|0">   • 18.8. Estorno - Alvar&#225;s</option>
						<option value="-308|0">   • 18.9. Estorno - Sindicato patronal</option>
						<option value="-119|0">19. Empr&#233;stimos</option>
						<option value="-315|0">   • 19.4. Estorno de pagamento de empr&#233;stimos</option>
						<option value="-316|0">   • 19.5. Estorno de pagamento de juros de empr&#233;stimos</option>
						<option value="-317|0">   • 19.6. Estorno - Outros</option>
						<option value="-121|0">2. Venda de material did&#225;tico</option>
						<option value="-318|0">   • 2.1. Receita na revenda de livros (franquia)</option>
						<option value="-319|0">   • 2.2. Receita na revenda de livros (escola)</option>
						<option value="-320|0">   • 2.3. Receita revenda livro franquia d&#233;b anteriores</option>
						<option value="-321|0">   • 2.4. Receita de juros e multa de livros (franquia)</option>
						<option value="-322|0">   • 2.5. Receita de juros e multa de livros (escola)</option>
						<option value="-323|0">   • 2.6. Receita de troco de livros (franquia)</option>
						<option value="-324|0">   • 2.7. Receita de troco de livros (escola)</option>
						<option value="-122|0">20. Renegocia&#231;&#245;es</option>
						<option value="-334|0">   • 20.10. Estorno pagamento  renegocia&#231;&#245;es - WLE</option>
						<option value="-330|0">   • 20.6. Estorno  pagamento renegocia&#231;&#245;es Aluguel</option>
						<option value="-331|0">   • 20.7. Estorno pag renegocia&#231;&#227;o Banco Financeira</option>
						<option value="-332|0">   • 20.8. Estorno pag renegocia&#231;&#245;es - Fornecedores</option>
						<option value="-333|0">   • 20.9. Estorno pagamento renegocia&#231;&#245;es - Impostos</option>
						<option value="-124|0">21. Pagamento de Imposto de Renda Pessoa Juridica</option>
						<option value="-336|0">   • 21.2. Estorno de IRPJ</option>
						<option value="-126|0">23. Transfer&#234;ncia de saldo entre caixas</option>
						<option value="-338|0">   • 23.2. Transfer&#234;ncia saldo entre caixas (entrada)</option>
						<option value="-128|0">24. Incorpora&#231;&#227;o de saldo</option>
						<option value="-341|0">   • 24.2. Incorpora&#231;&#227;o de saldo (entrada)</option>
						<option value="-130|0">25.Transfer&#234;ncia de saldo (banco)</option>
						<option value="-343|0">   • 25.2. Retorno de cheque devolvido do banco</option>
						<option value="-344|0">   • 25.3. Receita  estorno  cart&#227;o cr&#233;dito (entrada)</option>
						<option value="-345|0">   • 25.4. Transfer&#234;ncia de saldo do banco (entrada)</option>
						<option value="-347|0">   • 25.6 Receita com troca de cheque devolvido</option>
						<option value="-132|0">26. Cancelamento de opera&#231;&#227;o</option>
						<option value="-349|0">   • 26.2. Exclus&#227;o de pagamento do t&#237;tulo</option>
						<option value="-134|0">27. Diferen&#231;a de caixa</option>
						<option value="-422|0">   • 27.1. Diferen&#231;a de caixa a maior</option>
						<option value="-425|0">   • 27.3. Estorno de diferen&#231;a de caixa a menor</option>
						<option value="-136|0">3. Outras receitas</option>
						<option value="-350|0">   • 3.1. Receita de taxas</option>
						<option value="-351|0">   • 3.2. Receita revenda produtos ICMS</option>
						<option value="-352|0">   • 3.3. Receita de juros e multa - taxas</option>
						<option value="-353|0">   • 3.4. Receita  juros e multa - produtos  ICMS</option>
						<option value="-354|0">   • 3.5. Receita de troco - taxas</option>
						<option value="-355|0">   • 3.6. Receita de troco - produtos sujeitos a ICMS</option>
						<option value="-356|0">   • 3.7. Outras receitas</option>
						<option value="1000|0">   • 3.8. 2&#176; Chamada de Prova</option>
						<option value="-137|0">4. Receita n&#227;o operacional</option>
						<option value="-357|0">   • 4.1. Outras receitas n&#227;o operacionais</option>
						<option value="-139|0">6. Compra de material did&#225;tico</option>
						<option value="-372|0">   • 6.5. Estorno pagamento material did&#225;tico franquia</option>
						<option value="-373|0">   • 6.6. Estorno frete  material did&#225;tico franquia</option>
						<option value="-374|0">   • 6.7. Estorno pagamento material did&#225;tico escola</option>
						<option value="-375|0">   • 6.8. Estorno frete material did&#225;tico (escola)</option>
						<option value="-141|0">7. Compra de de produtos sujeitos a ICMS</option>
						<option value="-378|0">   • 7.3. Estorno  pagamento  produtos  ICMS</option>
						<option value="-379|0">   • 7.4. Estorno de frete com produtos sujeitos a ICMS</option>
						<option value="1003|0">7.5. Estorno de frete</option>
						<option value="-143|0">8. Folha pedag&#243;gica</option>
						<option value="-389|0">   • 8.10. Estorno - Outros</option>
						<option value="-385|0">   • 8.6. Estorno de sal&#225;rio - professores</option>
						<option value="-386|0">   • 8.7. Estorno de sal&#225;rio - coordenador de ensino</option>
						<option value="-387|0">   • 8.8. Estorno de comiss&#245;es - professores</option>
						<option value="-388|0">   • 8.9. Estorno de comiss&#245;es - coordenador de ensino</option>
						<option value="-145|0">9. Encargos pedag&#243;gicos</option>
						<option value="-406|0">   • 9.17. Estorno de hora extra professores</option>
						<option value="-407|0">   • 9.18. Estorno de hora extra coordenador de ensino</option>
						<option value="-408|0">   • 9.19. Estorno de vale-transporte professores</option>
						<option value="-409|0">   • 9.20. Estorno vale-transporte coord ensino</option>
						<option value="-410|0">   • 9.21. Estorno de vale-alimenta&#231;&#227;o professores</option>
						<option value="-411|0">   • 9.22. Estorno vale-alimenta&#231;&#227;o coord ensino</option>
						<option value="-412|0">   • 9.23. Estorno de plano de sa&#250;de professores</option>
						<option value="-413|0">   • 9.24. Estorno  plano sa&#250;de coordenador de ensino</option>
						<option value="-414|0">   • 9.25. Estorno de f&#233;rias professores</option>
						<option value="-415|0">   • 9.26. Estorno de f&#233;rias coordenador de ensino</option>
						<option value="-416|0">   • 9.27. Estorno de 13&#186; professores</option>
						<option value="-417|0">   • 9.28. Estorno de 13&#186; coordenador de ensino</option>
						<option value="-418|0">   • 9.29. Estorno de  INSS empregador professores</option>
						<option value="-419|0">   • 9.30. Estorno  INSS empregador coord ensino</option>
						<option value="-420|0">   • 9.31. Estorno de FGTS professores</option>
						<option value="-421|0">   • 9.32. Estorno de FGTS coordenador de ensino</option>
						<option value="894|0">Bonus -  Estacionamento Cart&#227;o</option>
						<option value="895|0">Bonus -  Estacionamento Dinheiro</option>
						<option value="997|0">BONUS - Estacionamento </option>
						<option value="-1|0">Devolu&#231;&#227;o de Cheques</option>
						<option value="-53|0">Estorno de Parcelas</option>
						<option value="-7|0">Misto</option>
						<option value="-51|0">Taxa Matr&#237;cula</option>
						<option value="-5|0">Transfer&#234;ncia</option>
						<option value="-3|0">Troco</option>

					</select>  
                                        </div>
                                        <div style="float: left; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label12" class="control-label">Nº Contrato:</span>
                                            <br />
                                            <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtNumeroContrato" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtNumeroContrato" class="form-control input-sm" style="width:100px;" />
                                        </div>
                                        <div style="float: left; display: table-cell;">
                                            &nbsp;
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label10" class="control-label">Nº do Recibo:</span>
                                            <br />
                                            &nbsp;
                                            <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtNumeroRecibo" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtNumeroRecibo" class="form-control input-sm" style="width:100px;" />
                                        </div>
                                        
                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel2" style="width:260px;">
						<fieldset>
							<legend>
								Vencimento entre
							</legend>
                                                
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />

<input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdVencimentoInicial$txtData" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_txtData" class="form-control input-sm" data-calendario="true" style="width:85px;" />
<a id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_btnCalendar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdVencimentoInicial$btnCalendar&#39;,&#39;&#39;)"><i id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_image1" class="fa fa-calendar-days CorMenuItem" alt="V" style="cursor: pointer; font-size: 16px; margin-left: 5px;"></i></a>
<input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdVencimentoInicial$mask_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_mask_ClientState" />


                                                <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label15" class="control-label">   e   </span>
                                                
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />

<input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdVencimentoFinal$txtData" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_txtData" class="form-control input-sm" data-calendario="true" style="width:85px;" />
<a id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_btnCalendar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdVencimentoFinal$btnCalendar&#39;,&#39;&#39;)"><i id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_image1" class="fa fa-calendar-days CorMenuItem" alt="V" style="cursor: pointer; font-size: 16px; margin-left: 5px;"></i></a>
<input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdVencimentoFinal$mask_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_mask_ClientState" />


                                            
						</fieldset>
					</div>
                                        </div>
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel3" style="width:260px;">
						<fieldset>
							<legend>
								Pagamento entre
							</legend>
                                                
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />

<input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdPagamentoInicial$txtData" type="text" value="01/11/2025" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_txtData" class="form-control input-sm" data-calendario="true" style="width:85px;" />
<a id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_btnCalendar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdPagamentoInicial$btnCalendar&#39;,&#39;&#39;)"><i id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_image1" class="fa fa-calendar-days CorMenuItem" alt="V" style="cursor: pointer; font-size: 16px; margin-left: 5px;"></i></a>
<input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdPagamentoInicial$mask_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_mask_ClientState" />


                                                <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label7" class="control-label">   e   </span>
                                                
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />

<input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdPagamentoFinal$txtData" type="text" value="31/12/2026" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_txtData" class="form-control input-sm" data-calendario="true" style="width:85px;" />
<a id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_btnCalendar" class="link" href="javascript:__doPostBack(&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdPagamentoFinal$btnCalendar&#39;,&#39;&#39;)"><i id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_image1" class="fa fa-calendar-days CorMenuItem" alt="V" style="cursor: pointer; font-size: 16px; margin-left: 5px;"></i></a>
<input type="hidden" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$wcdPagamentoFinal$mask_ClientState" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_mask_ClientState" />


                                            
						</fieldset>
					</div>
                                        </div>
                                        <div style="float: left; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label5" class="control-label">Nº do Cheque:</span>
                                            <br />
                                            <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtNumeroCheque" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtNumeroCheque" class="form-control input-sm" style="width:100px;" />
                                        </div>
                                        <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_divFiltroCarne" style="float: left; width: 120px; display: table-cell;">
                                            &nbsp;
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label8" class="control-label">Nº do carnê:</span>
                                            <br />
                                            &nbsp;
                                            <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtNumeroCarne" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtNumeroCarne" class="form-control input-sm" style="width:100px;" />
                                        </div>
                                        
                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel7" style="width:260px;">
						<fieldset>
							<legend>
								Nº do carnê entre
							</legend>
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtCarneInicial" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtCarneInicial" class="form-control input-sm" style="width:110px;" />
                                                
                                                <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label14" class="control-label">   e   </span>
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtCarneFinal" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtCarneFinal" class="form-control input-sm" style="width:110px;" />
                                                
                                            
						</fieldset>
					</div>
                                        </div>
                                        <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_divFiltroLayout" style="float: left; width: 300px; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label6" class="control-label">Layout de Cobrança:</span>
                                            <br />
                                            <select name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cmbConta" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cmbConta" class="combo" style="width:260px;">
						<option selected="selected" value="0">(Selecione)</option>
						<option value="5">Boletos sem Cedente associado (240) - 012345 - Carteira DM</option>

					</select>
                                        </div>
                                        <div style="float: left; display: table-cell;">
                                            <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_lblSituacaoAluno" class="control-label">Situação do Aluno</span>
                                            <br />
                                            <select name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cmbSituacoesAlunos" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cmbSituacoesAlunos" class="combo" style="width:200px;">
						<option selected="selected" value="0">(Selecione)</option>
						<option value="-1">Ativo</option>
						<option value="-5">Desistente</option>
						<option value="-4">Formado</option>
						<option value="-2">Inativo</option>
						<option value="-3">Interessado</option>
						<option value="-6">Matr&#237;cula Trancada</option>
						<option value="-10">Rematriculado</option>
						<option value="2">Transferido</option>

					</select>
                                        </div>
                                        
                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel5" style="width:260px;">
						<fieldset>
							<legend>
								Nº de boleto entre
							</legend>
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtBoletoInicial" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtBoletoInicial" class="form-control input-sm" style="width:110px;" />
                                                
                                                <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label9" class="control-label">   e   </span>
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtBoletoFinal" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtBoletoFinal" class="form-control input-sm" style="width:110px;" />
                                                
                                            
						</fieldset>
					</div>
                                        </div>
                                        <div style="float: left; width: 300px; display: table-cell;">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_pnpValoresEntre" style="width:260px;">
						<fieldset>
							<legend>
								Valor entre:
							</legend>
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtValorInicial" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtValorInicial" class="form-control input-sm" style="width:110px;" />
                                                
                                                <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_lblE" class="control-label">   e   </span>
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtValorFinal" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtValorFinal" class="form-control input-sm" style="width:110px;" />
                                                
                                            
						</fieldset>
					</div>
                                        </div>
                                        
                                        
                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: left">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_pnlFormasCobrança" style="width:260px;">
						<fieldset>
							<legend>
								Formas de Cobrança:
							</legend>
                                                <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkMarcarFormasCobranca" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$chkMarcarFormasCobranca" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$chkMarcarFormasCobranca\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkMarcarFormasCobranca">Marcar Todas</label></span>
                                                <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel13" style="height:150px;width:100%;overflow-y:scroll;">
								
                                                    <table id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas" border="0">
									<tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_0" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$0" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_0">Crédito Sponte Pay</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_1" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$1" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_1">Débito Automático</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_2" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$2" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_2">Cartão de Débito</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_3" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$3" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_3">Cartão de Crédito</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_4" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$4" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_4">Cobrança Bancária</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_5" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$5" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_5">Cheque Pré-Datado</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_6" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$6" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_6">Cheque</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_7" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$7" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_7">Dinheiro</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_8" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$8" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_8">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_9" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$9" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_9">Boleto</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_10" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$10" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_10">Deposito em conta</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_11" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblCobrancas$11" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblCobrancas_11">Pix - Centro Logístico Ag:0843 C/c 33.200-3</label></span></td>
									</tr>
								</table>
                                                
							</div>
                                            
						</fieldset>
					</div>
                                        </div>
                                        <div style="float: left; width: 17%; margin-left: 48px">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_pnlTipoRecebimento" style="width:260px;">
						<fieldset>
							<legend>
								Tipo de Recebimento:
							</legend>
                                                <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkMarcarTodasTipoRecebimento" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$chkMarcarTodasTipoRecebimento" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$chkMarcarTodasTipoRecebimento\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkMarcarTodasTipoRecebimento">Marcar Todas</label></span>
                                                <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkMarcarInativosTipoRecebimento" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$chkMarcarInativosTipoRecebimento" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$chkMarcarInativosTipoRecebimento\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkMarcarInativosTipoRecebimento">Mostrar Inativos</label></span>
                                                <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel14" style="height:150px;width:100%;overflow-y:scroll;">
								
                                                    <table id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento" border="0">
									<tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_0" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$0" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_0">Crédito Sponte Pay</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_1" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$1" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_1">Cartão de Débito</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_2" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$2" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_2">Cartão de Crédito</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_3" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$3" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_3">Cobrança Bancária</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_4" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$4" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_4">Dinheiro</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_5" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$5" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_5">Pix - Bradesco Mensalidades Ag: 0843 C/c 29368-7</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_6" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$6" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_6">Boleto</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_7" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$7" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_7">Deposito em conta</label></span></td>
									</tr><tr>
										<td><span><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_8" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cblRecebimento$8" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cblRecebimento_8">Pix - Centro Logístico Ag:0843 C/c 33.200-3</label></span></td>
									</tr>
								</table>
                                                
							</div>
                                            
						</fieldset>
					</div>
                                        </div>
                                        <div style="float: left; width: 17%; margin-left: 48px">
                                            <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel11">
						<fieldset>
							<legend>
								Situação
							</legend>
                                                <div>
                                                    <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbPendentes" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cbPendentes" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbPendentes">Pendentes</label></span>
                                                </div>
                                                <div>
                                                    <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbQuitadas" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cbQuitadas" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbQuitadas">Quitadas</label></span>
                                                </div>
                                                <div>
                                                    <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbCanceladas" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cbCanceladas" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbCanceladas">Canceladas</label></span>
                                                </div>
                                                <br />
                                                <br />
                                                <div id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Panel10">
								<fieldset>
									<legend>
										Pendentes
									</legend>
                                                    <div style="float: left;">
                                                        <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbVencidas" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cbVencidas" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbVencidas">Vencidas</label></span>
                                                        <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbNegativadas" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$cbNegativadas" onclick="javascript:setTimeout(&#39;__doPostBack(\&#39;ctl00$ContentPlaceHolder1$tab$tabFiltro$cbNegativadas\&#39;,\&#39;\&#39;)&#39;, 0)" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_cbNegativadas">Negativadas</label></span>
                                                    </div>
                                                    
                                                
								</fieldset>
							</div>
                                            
						</fieldset>
					</div>
                                            <div style="float: left; display: table-cell; margin-top: 15%;">
                                                <span id="ctl00_ContentPlaceHolder1_tab_tabFiltro_Label4" class="control-label">Complemento:</span>
                                                <br />
                                                <input name="ctl00$ContentPlaceHolder1$tab$tabFiltro$txtComplemento" type="text" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_txtComplemento" class="form-control input-sm" style="width:260px;" />
                                            </div>
                                        </div>

                                        <div style="float: left; width: 300px; margin-left: 20px; padding: 8px">
                                            <span class="checkbox checkbox-primary d-inline-flex"><input id="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkParcelasRematricula" type="checkbox" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$chkParcelasRematricula" /><label for="ctl00_ContentPlaceHolder1_tab_tabFiltro_chkParcelasRematricula">Parcelas de rematrículas</label></span>
                                        </div>
                                        
                                    </div>
                                    <br />
                                    <div style="clear: both; width: 100%; display: table;">
                                        <div style="float: right;">
                                            <div id='ctl00_ContentPlaceHolder1_tab_tabFiltro_btnFiltrar_div' tabindex="0" class='btn btn-outline-primary' style="" onclick="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;clickButton($get('ctl00_ContentPlaceHolder1_tab_tabFiltro_btnFiltrar'));" onkeydown="if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;if ((event.which || event.keyCode) && (event.keyCode == 13 || event.keyCode == 32)){event.returnValue=false;event.cancel = true;clickButton(this);}" onmousedown="javascript:this.getElementsByTagName('div')[0].style.marginTop = '2px';this.getElementsByTagName('div')[0].style.marginLeft = '2px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseover="javascript:this.className='btn btn-outline-primary btn btn-outline-primary_hover';" onmouseup="javascript:this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;" onmouseout="javascript:this.className='btn btn-outline-primary';this.getElementsByTagName('div')[0].style.marginTop = '0px';this.getElementsByTagName('div')[0].style.marginLeft = '0px';if(Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) return false;"><div class='div_name_text' style='margin-top:0px; margin-left:0px;'><center><div style="float: left;" class='fa fa-search topimg'></div><span class ='btn btn-outline-primary_text'> Filtrar </span></center></div>
</div><input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$btnFiltrar" value="Filtrar" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_btnFiltrar" class="btn btn-outline-primary" style="display:none;" />
                                        </div>
                                    </div>
                                
				</div>
                                <input type="submit" name="ctl00$ContentPlaceHolder1$tab$tabFiltro$btnCarregaFiltrosAvancados" value="" id="ctl00_ContentPlaceHolder1_tab_tabFiltro_btnCarregaFiltrosAvancados" class="btn btn-outline-secondary btn-sm btn-custom" CssImageClass="fa" CssTextClass="btn-sm" CssDisabledClass="btn btn-sm btn-outline-secondary disabled" aria-disabled="true" style="visibility: hidden;" />
                            
			</div>
                    
		</div>
	</div>
</div>
        |0|hiddenField|__EVENTTARGET||0|hiddenField|__EVENTARGUMENT||0|hiddenField|__LASTFOCUS||24|hiddenField|__VIEWSTATE_KEY|6aa337fbbe07ce014098ebc5|0|hiddenField|__VIEWSTATE||0|hiddenField|__VIEWSTATEENCRYPTED||732|asyncPostBackControlIDs||ctl00$lnkSelecionaempresa,lnkSelecionaempresa,ctl00$ContentPlaceHolder1$tab,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnAtualizaGrid,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnNovo,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnEditar,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnDetalhes,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnExcluir,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnQuitar,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnRecibo,,ctl00$ContentPlaceHolder1$tab$tabGrid$btnFiltroRapido,,ctl00$ContentPlaceHolder1$tab$tabFiltro$rblSacado,,ctl00$ContentPlaceHolder1$tab$tabFiltro$rblResponsavel,,ctl00$ContentPlaceHolder1$tab$tabFiltro$btnFiltrar,,ctl00$ContentPlaceHolder1$tab$tabFiltro$btnCarregaFiltrosAvancados,,ctl00$btnMostrarAvisos,|0|postBackControlIDs|||788|updatePanelIDs||tctl00$updNovoMenu,,tctl00$updateAutoComplete,,tctl00$updMatriculaWeb,,tctl00$updMatriculaWebCCAA,,tctl00$UpdatePanel1,,tctl00$ContentPlaceHolder1$updGlobal,,tctl00$ContentPlaceHolder1$tab$tabGrid$updGrid,,tctl00$ContentPlaceHolder1$tab$tabGrid$updAbrir,,tctl00$ContentPlaceHolder1$tab$tabGrid$updExcluir,,tctl00$ContentPlaceHolder1$tab$tabGrid$updQuitar,,tctl00$ContentPlaceHolder1$tab$tabGrid$UpdateModalProcessamento,,tctl00$ContentPlaceHolder1$tab$tabGrid$updRecibo,,tctl00$ContentPlaceHolder1$tab$tabGrid$updFiltroRapido,,tctl00$ContentPlaceHolder1$tab$tabGrid$updResumo,,tctl00$ContentPlaceHolder1$tab$tabFiltro$updAC,,tctl00$ContentPlaceHolder1$tab$tabFiltro$updFiltro,,tctl00$mwMatriculaWeb$updGeral,,tctl00$mwMatriculaWebCCAA$updGeral,,tctl00$updBotaoAvisos,,tctl00$updAvisosERP,|498|childUpdatePanelIDs||ctl00$ContentPlaceHolder1$tab$tabGrid$updGrid,ctl00$ContentPlaceHolder1$tab$tabGrid$updAbrir,ctl00$ContentPlaceHolder1$tab$tabGrid$updExcluir,ctl00$ContentPlaceHolder1$tab$tabGrid$updQuitar,ctl00$ContentPlaceHolder1$tab$tabGrid$UpdateModalProcessamento,ctl00$ContentPlaceHolder1$tab$tabGrid$updRecibo,ctl00$ContentPlaceHolder1$tab$tabGrid$updFiltroRapido,ctl00$ContentPlaceHolder1$tab$tabGrid$updResumo,ctl00$ContentPlaceHolder1$tab$tabFiltro$updAC,ctl00$ContentPlaceHolder1$tab$tabFiltro$updFiltro|36|panelsToRefreshIDs||ctl00$ContentPlaceHolder1$updGlobal,|3|asyncPostBackTimeout||600|20|formAction||./ContasReceber.aspx|29|pageTitle||Sponte Web - Contas a Receber|179|scriptBlock|ScriptContentNoTags|function quitar(){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}|141|scriptBlock|ScriptContentNoTags|function selecionados(){return GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd').length > 0 ? '' : 'Nenhum registro selecionado!'}|424|scriptBlock|ScriptContentNoTags|function editar(){var err = selecionados(); if (err.length == 0){var cID = GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')[0];var sacado = cID[2]; var nroParcela = cID[1]; cID = cID[0];openWindow(1, 'cadconrec' + cID, 'Editar Plano - ' + sacado, 'ContaReceberCadastro.aspx?id=' + cID + '&numParcela='+ nroParcela, false, 610, 780, true, false, false, null);}else{if (err != 'err') { alert(err); } return 'err'}}|180|scriptBlock|ScriptContentNoTags|function excluir(){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}|181|scriptBlock|ScriptContentNoTags|function cancelar(){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}|292|scriptBlock|ScriptContentNoTags|function recibo(){var err = selecionados(); if (err.length == 0){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}else{if (err!='err' && err != false) {alert(err);} return false;}}|296|scriptBlock|ScriptContentNoTags|function impBoletos(){var err = selecionados(); if (err.length == 0){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}else{if (err!='err' && err != false) {alert(err);} return false;}}|540|scriptBlock|ScriptContentNoTags|function fRenegociarVerificaAguardandoPagamentoBoleto(){var parcelaStatus; parcelaStatus = (GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd').length > 0 ? GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')[0][5] : 0); var parcelaAguardandoPagamentoBoleto; parcelaAguardandoPagamentoBoleto = GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')[0][10]; return (parcelaStatus == 0 && parcelaAguardandoPagamentoBoleto > 0) ? 'Não é possível renegociar uma parcela que esta aguardando o pagamento do boleto.' : '' }|560|scriptBlock|ScriptContentNoTags|function renegociacao(){var err = fRenegociarVerificaAguardandoPagamentoBoleto(); if (err.length == 0){var aluno; aluno = (GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd').length > 0 ? GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')[0][3] : 0);(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd').length > 0 && aluno == 0) ? window.alert('A renegociação de parcelas só está disponível para alunos.') : window.open('../SPAssist/Renegociacao.aspx?aluno=' + aluno, '_blank');}else{if (err != 'err') { alert(err); } return 'err'}}|244|scriptBlock|ScriptContentNoTags|function validaQuitada(){var err = selecionados(); if (err.length == 0){return GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')[0][5] == 1 ? '' : 'Selecione uma parcela quitada.'}else{if (err != 'err') { alert(err); } return 'err'}}|255|scriptBlock|ScriptContentNoTags|function validaApenasUma(){var err = validaQuitada(); if (err.length == 0){return GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd').length == 1 ? '' : 'Selecione apenas uma parcela quitada.'}else{if (err != 'err') { alert(err); } return 'err'}}|286|scriptBlock|ScriptContentNoTags|function detalhes(){var err = validaApenasUma(); if (err.length == 0){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')[0].join('|');return true;}else{if (err!='err' && err != false) {alert(err);} return false;}}|300|scriptBlock|ScriptContentNoTags|function recibobematech(){var err = selecionados(); if (err.length == 0){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}else{if (err!='err' && err != false) {alert(err);} return false;}}|194|scriptBlock|ScriptContentNoTags|function cNegativar(){var err = selecionados(); if (err.length == 0){return (confirm('Confirma a negativação das parcelas?')) ? '' : 'err' ;}else{if (err != 'err') { alert(err); } return 'err'}}|293|scriptBlock|ScriptContentNoTags|function negativar(){var err = cNegativar(); if (err.length == 0){$get('ctl00_ContentPlaceHolder1_tab_tabGrid_hiddenID').value = retListaKeys(GetSelectedKeys('ctl00_ContentPlaceHolder1_tab_tabGrid_grd')).join('|');return true;}else{if (err!='err' && err != false) {alert(err);} return false;}}|128|scriptBlock|ScriptContentNoTags|function CallbackacFiltroMaster(arg, context) {WebForm_DoCallback('ctl00$acFiltroMaster',arg,ReceiveData,context,null,false); } |1017|scriptBlock|ScriptContentNoTags|if (window.__ExtendedControlCssLoaded == null || typeof window.__ExtendedControlCssLoaded == 'undefined') {    window.__ExtendedControlCssLoaded = new Array();}var controlCssLoaded = window.__ExtendedControlCssLoaded; var head = document.getElementsByTagName('HEAD')[0];if (head && !Array.contains(controlCssLoaded,'/WebResource.axd?d=gRfIWAYAKStFuv250my4nttX2moYAXuVAyD8EwgD2CvJ-_zQsaxoQRCPxFwBb_zcnGOmqT87Eg25UkX1dBn9plSTrc5u2kB085_Uxgj-NhhrBEObg27bzLvZvLkkZDPN0&t=639244719320000000')) {var linkElement = document.createElement('link');linkElement.type = 'text/css';linkElement.rel = 'stylesheet';linkElement.href = '/WebResource.axd?d=gRfIWAYAKStFuv250my4nttX2moYAXuVAyD8EwgD2CvJ-_zQsaxoQRCPxFwBb_zcnGOmqT87Eg25UkX1dBn9plSTrc5u2kB085_Uxgj-NhhrBEObg27bzLvZvLkkZDPN0&t=639244719320000000';head.appendChild(linkElement);controlCssLoaded.push('/WebResource.axd?d=gRfIWAYAKStFuv250my4nttX2moYAXuVAyD8EwgD2CvJ-_zQsaxoQRCPxFwBb_zcnGOmqT87Eg25UkX1dBn9plSTrc5u2kB085_Uxgj-NhhrBEObg27bzLvZvLkkZDPN0&t=639244719320000000');}|27|scriptBlock|ScriptPath|../Scripts/DateFunctions.js|1083|scriptBlock|ScriptContentNoTags|if (window.__ExtendedControlCssLoaded == null || typeof window.__ExtendedControlCssLoaded == 'undefined') {    window.__ExtendedControlCssLoaded = new Array();}var controlCssLoaded = window.__ExtendedControlCssLoaded; var head = document.getElementsByTagName('HEAD')[0];if (head && !Array.contains(controlCssLoaded,'/WebResource.axd?d=QygwMQZzIIofqDLXDr-HEOqJytnRlPKClTuWi_4ehXzbS0Z69dElxzDVaFRuAwSaJYf3RQnYABBsgmSb5hykRfe0FPjWBRJQMFYt7RRwGi88n6UCkYFr1e09BvpmYYamTQi5krPExR9kylYcsemssQ2&t=639244719320000000')) {var linkElement = document.createElement('link');linkElement.type = 'text/css';linkElement.rel = 'stylesheet';linkElement.href = '/WebResource.axd?d=QygwMQZzIIofqDLXDr-HEOqJytnRlPKClTuWi_4ehXzbS0Z69dElxzDVaFRuAwSaJYf3RQnYABBsgmSb5hykRfe0FPjWBRJQMFYt7RRwGi88n6UCkYFr1e09BvpmYYamTQi5krPExR9kylYcsemssQ2&t=639244719320000000';head.appendChild(linkElement);controlCssLoaded.push('/WebResource.axd?d=QygwMQZzIIofqDLXDr-HEOqJytnRlPKClTuWi_4ehXzbS0Z69dElxzDVaFRuAwSaJYf3RQnYABBsgmSb5hykRfe0FPjWBRJQMFYt7RRwGi88n6UCkYFr1e09BvpmYYamTQi5krPExR9kylYcsemssQ2&t=639244719320000000');}|150|scriptBlock|ScriptContentNoTags|function CallbackacSacado(arg, context) {WebForm_DoCallback('ctl00$ContentPlaceHolder1$tab$tabFiltro$acSacado',arg,ReceiveData,context,null,false); } |160|scriptBlock|ScriptContentNoTags|function CallbackacResponsavel(arg, context) {WebForm_DoCallback('ctl00$ContentPlaceHolder1$tab$tabFiltro$acResponsavel',arg,ReceiveData,context,null,false); } |91|scriptBlock|ScriptPath|/SPFin/ContasReceber.aspx?_TSM_HiddenField_=ctl00_scm_HiddenField&_TSM_CombinedScripts_=%3b|98|scriptStartupBlock|ScriptContentNoTags|try{$1('select[PermiteIncluir!=true]').select2();}catch(e){};try{AplicaCor('#0D4272');}catch(x){};|1752|scriptStartupBlock|ScriptContentNoTags|$(document).ready(function() { $('<div class="maxzindex modal fade" id="processing-modal" tabindex="-1" role="dialog" data-bs-backdrop="Static" data-bs-keyboard="false" aria-labelledby="processing-modal" aria-hidden="True" style="top:35%;"><div class="modal-dialog" role="document"><div class="spinner"><div class="bounce1"></div><div class="bounce2"></div><div class="bounce3"></div></div></div></div>').appendTo('body'); }); $( "input[name*='wcd']").addClass("newwcd");$('<script>try{var prm = Sys.WebForms.PageRequestManager.getInstance();         prm.add_beginRequest(beginRequest);         prm.add_endRequest(endRequest); }catch(x){};        function beginRequest(sender, args) {             showLoader();         }         function endRequest(sender, args) {             setTimeout(function() { hideLoader(); }, 100);         }         function showLoader() {            $("#processing-modal").modal("show"); $("#processing-modal").attr("data-bs-backdrop", "static");  $("#processing-modal").attr("data-bs-keyboard", "false");        }         function hideLoader() {            $("#processing-modal").modal("hide");            setTimeout(function() {                $(".modal-backdrop").remove();                $("#processing-modal").css("display","none");                $("body").removeClass("modal-open");            }, 300);         } <\/script>').appendTo('body'); $('.filtroAntigo').hide();  $('.imagemCalendario').next('i').remove(); $('.imagemCalendario').hide(); if(!$('.imagemCalendario').next('i').length) { $('.imagemCalendario').after('<i class="fa fa-calendar corCalendario"></i>'); }jQuery('[data-calendario="true"]').css('width', '90px');$('.combo').select2().on('change', function (e) {try{onClickSelect2(this);}catch(e){}; });|648|scriptStartupBlock|ScriptContentNoTags|$(function(){  $('.gridRow').dblclick(function(e){var k = this.getAttribute('keys').split("|");var cID = k[0];var nroParcela = k[1];var sacado = k[2];openWindow(1, 'cadconrec' + cID , 'Editar Plano - ' + sacado, 'ContaReceberCadastro.aspx?id=' + cID + '&numParcela='+ nroParcela, false, 610, 780, true, false, false, null);});$('.gridAlternateRow').dblclick(function(){var k = this.getAttribute('keys').split("|");var cID = k[0];var nroParcela = k[1];var sacado = k[2];openWindow(1, 'cadconrec' + cID , 'Editar Plano - ' + sacado, 'ContaReceberCadastro.aspx?id=' + cID + '&numParcela='+ nroParcela, false, 610, 780, true, false, false, null);});});|247|scriptStartupBlock|ScriptContentNoTags|(function() { try { var n = Sys.Extended.UI.MaskedEditBehavior.prototype, t = n._ExecuteNav; n._ExecuteNav = function(n) { var i = n.type; i == "keydown" && (n.type = "keypress"), t.apply(this, arguments), n.type = i } } catch (i) { return } })();|102|scriptStartupBlock|ScriptContentNoTags|var oAvisoLead=$get('ctl00_wavLead_pnlAvisosLead'); if (oAvisoLead) {oAvisoLead.style.display='none';}|172|scriptStartupBlock|ScriptContentNoTags|var oAviso=$get('ctl00_wavAvisos_pnlAvisos'); var sleft; if (oAviso) {sleft=(eval(oAviso.style['left'].replace('px',''))+200).toString()+'px'; oAviso.style['left']=sleft;} |24|scriptStartupBlock|ScriptContentNoTags|$('select').select2({});|219|scriptStartupBlock|ScriptContentWithTags|{"text":"","src":"/WebResource.axd?d=v574ibSHXkDzoHFjCVgEbbFVsOnlbXau3WY6nhd-YXFhbGQeqcB3_TMB5JMGm9RHWMK6gJkhAqJWRnvD95DMjzeRo_eGUK4sHq1JMbtJKUH3ypw2hGkadUA_lnfvK7_q0\u0026t=639244719340000000","type":"text/javascript"}|219|scriptStartupBlock|ScriptContentWithTags|{"text":"","src":"/WebResource.axd?d=JnXcQnhyw4l8168GF0XBt_HfhcYY9gOSAXskEjMdwn2n7ZB6jNFXQe3VsJqScOKd2mZ3Ke9vXQzHkNh08dU6X-CGErnKPFDpMOS1SZUGISAIpTMZhNGqpbdxlNUF5tYy0\u0026t=639244719340000000","type":"text/javascript"}|66|scriptStartupBlock|ScriptContentNoTags|registerInputEvents('ctl00_acFiltroMaster_acFiltroMasterTextBox');|179|scriptStartupBlock|ScriptContentNoTags|acFiltroMasterMinLength='3';loadingacFiltroMaster=false;acFiltroMasterAutoPostBack=false;acFiltroMasterSubmitOnEnter=false;acFiltroMasterMaxHeight=0;acFiltroMasterDisplayCount=15;|88|scriptStartupBlock|ScriptContentNoTags|registerInputEvents('ctl00_ContentPlaceHolder1_tab_tabFiltro_acSacado_acSacadoTextBox');|143|scriptStartupBlock|ScriptContentNoTags|acSacadoMinLength='3';loadingacSacado=false;acSacadoAutoPostBack=false;acSacadoSubmitOnEnter=false;acSacadoMaxHeight=0;acSacadoDisplayCount=15;|98|scriptStartupBlock|ScriptContentNoTags|registerInputEvents('ctl00_ContentPlaceHolder1_tab_tabFiltro_acResponsavel_acResponsavelTextBox');|173|scriptStartupBlock|ScriptContentNoTags|acResponsavelMinLength='4';loadingacResponsavel=false;acResponsavelAutoPostBack=false;acResponsavelSubmitOnEnter=false;acResponsavelMaxHeight=0;acResponsavelDisplayCount=15;|23|scriptStartupBlock|ScriptContentNoTags|__defaultFired = false;|391|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.ModalPopupBehavior, {"BackgroundCssClass":"modalBackground","DropShadow":true,"PopupControlID":"ctl00_ContentPlaceHolder1_tab_tabGrid_pnlDetalhes","dynamicServicePath":"/SPFin/ContasReceber.aspx","id":"mpeDetalhesBehaviorID","repositionMode":2}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabGrid_LinkButton2"));
});
|646|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_mask_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"99/99/9999","MaskType":1,"id":"ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_mask"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_txtData"));
});
|418|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CalendarBehavior, {"button":$get("ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_btnCalendar"),"format":"dd/MM/yyyy","id":"ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_calendarButtonExtender","popupPosition":1}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoInicial_txtData"));
});
|640|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_mask_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"99/99/9999","MaskType":1,"id":"ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_mask"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_txtData"));
});
|412|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CalendarBehavior, {"button":$get("ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_btnCalendar"),"format":"dd/MM/yyyy","id":"ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_calendarButtonExtender","popupPosition":1}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabGrid_wcdVencimentoRapidoFinal_txtData"));
});
|289|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.TabPanel, {"headerTab":$get("__tab_ctl00_ContentPlaceHolder1_tab_tabGrid"),"ownerID":"ctl00_ContentPlaceHolder1_tab"}, null, {"owner":"ctl00_ContentPlaceHolder1_tab"}, $get("ctl00_ContentPlaceHolder1_tab_tabGrid"));
});
|596|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClearMaskOnLostFocus":false,"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabFiltro_maskCPF_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"999,999,999-99","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_maskCPF"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtCPF"));
});
|634|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_mask_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"99/99/9999","MaskType":1,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_mask"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_txtData"));
});
|406|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CalendarBehavior, {"button":$get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_btnCalendar"),"format":"dd/MM/yyyy","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_calendarButtonExtender","popupPosition":1}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoInicial_txtData"));
});
|628|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_mask_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"99/99/9999","MaskType":1,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_mask"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_txtData"));
});
|400|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CalendarBehavior, {"button":$get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_btnCalendar"),"format":"dd/MM/yyyy","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_calendarButtonExtender","popupPosition":1}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdVencimentoFinal_txtData"));
});
|631|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_mask_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"99/99/9999","MaskType":1,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_mask"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_txtData"));
});
|403|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CalendarBehavior, {"button":$get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_btnCalendar"),"format":"dd/MM/yyyy","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_calendarButtonExtender","popupPosition":1}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoInicial_txtData"));
});
|625|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.MaskedEditBehavior, {"ClientStateFieldID":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_mask_ClientState","CultureAMPMPlaceholder":"","CultureCurrencySymbolPlaceholder":"R$","CultureDateFormat":"DMY","CultureDatePlaceholder":"/","CultureDecimalPlaceholder":",","CultureName":"pt-BR","CultureThousandsPlaceholder":".","CultureTimePlaceholder":":","Mask":"99/99/9999","MaskType":1,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_mask"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_txtData"));
});
|397|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.CalendarBehavior, {"button":$get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_btnCalendar"),"format":"dd/MM/yyyy","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_calendarButtonExtender","popupPosition":1}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_wcdPagamentoFinal_txtData"));
});
|249|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.FilteredTextBoxBehavior, {"FilterType":2,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_filter5"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtCarneInicial"));
});
|247|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.FilteredTextBoxBehavior, {"FilterType":2,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_filter6"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtCarneFinal"));
});
|250|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.FilteredTextBoxBehavior, {"FilterType":2,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_filter1"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtBoletoInicial"));
});
|248|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.FilteredTextBoxBehavior, {"FilterType":2,"id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_filter2"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtBoletoFinal"));
});
|277|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.FilteredTextBoxBehavior, {"FilterType":3,"ValidChars":",","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_filterValorInicial"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtValorInicial"));
});
|273|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.FilteredTextBoxBehavior, {"FilterType":3,"ValidChars":",","id":"ctl00_ContentPlaceHolder1_tab_tabFiltro_filterValorFinal"}, null, null, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro_txtValorFinal"));
});
|320|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.TabPanel, {"headerTab":$get("__tab_ctl00_ContentPlaceHolder1_tab_tabFiltro"),"ownerID":"ctl00_ContentPlaceHolder1_tab"}, {"click":abriufiltrosAvancados}, {"owner":"ctl00_ContentPlaceHolder1_tab"}, $get("ctl00_ContentPlaceHolder1_tab_tabFiltro"));
});
|230|scriptStartupBlock|ScriptContentNoTags|Sys.Application.add_init(function() {
    $create(Sys.Extended.UI.TabContainer, {"activeTabIndex":0,"clientStateField":$get("ctl00_ContentPlaceHolder1_tab_ClientState")}, null, null, $get("ctl00_ContentPlaceHolder1_tab"));
});
|43|hiddenField|ctl00_ContentPlaceHolder1_tab_ClientState|{"ActiveTabIndex":0,"TabState":[true,true]}|