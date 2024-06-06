let select_len = document.querySelector('.select_len');
let _year_select = document.querySelector('._year_select')
let _month_select = document.querySelector('._month_select')
let button_year_chart;
let button_month_chart;
let select_year;
let month_table_select;
let month_select;
let year_select;

select_len.addEventListener('change', function() {
    let option = ``;
    let class_name = '';
    if (select_len.value == '1') {
        Object.keys(all_month).forEach(function(key) {
            option += `<option value="${key}">${key}</option>`;
        });
        class_name = 'year_table_select';
    }else if(select_len.value == '2'){
        Object.keys(all_month).forEach(function(key) {
            option += `<option value="${key}">${key}</option>`;
        });
        class_name = 'month_table_select';
    }else{
        _year_select.innerHTML = ``;
        _month_select.innerHTML = ``;
        return;
    }
    _month_select.innerHTML = ``;
    let selectHTML = ``;

    // form-select year_table_select
    // form-select month_table_select
    // form-select year_month_select
    if(class_name == 'month_table_select'){
        selectHTML = `
        <label for="formGroupExampleInput" class="form-label">輸入123份</label>
        <select class="form-select `+class_name+`" aria-label="Default select example" id="year">
        <option value="-1">請選擇年份</option>
        ` + option + `
        </select>
        `;
        _year_select.innerHTML = selectHTML;
    }else{
        selectHTML = `
        <label for="formGroupExampleInput" class="form-label">輸入年份</label>
        <div class="input-group">
        <select class="form-select `+class_name+`" aria-label="Default select example" id="year">
        <option value="-1">請選擇年份</option>
        ` + option + `
        </select>
        <button class="btn btn-outline-primary button_year_chart disabled" type="button">顯示圖表</button>
        </div>
        `;
        _year_select.innerHTML = selectHTML;
        button_year_chart = document.querySelector('.button_year_chart');
        button_year_chart.addEventListener('click', function() {
            console.log(document.querySelector('.'+class_name).value);
        });
    }
    
    
    if(class_name == 'year_table_select'){
        select_year = document.querySelector('.year_table_select');
        button_year_chart = document.querySelector('.button_year_chart');
        select_year.addEventListener('change', function() {
            if(select_year.value == '-1'){
                button_year_chart.classList.add('disabled');
            }else{
                button_year_chart.classList.remove('disabled');
            }

        });
    }else{
        month_table_select = document.querySelector('.month_table_select');
        month_table_select.addEventListener('change', function() {
            if(month_table_select.value == '-1'){
                _month_select.innerHTML = ``;
                return;
            }else{
                let option = ``;
                all_month[month_table_select.value].forEach(function(key) {
                    option += `<option value="${key}">${key}</option>`;
                });
                let selectHTML = `
                <label for="formGroupExampleInput" class="form-label">輸入月份</label>  
                <div class="input-group">
                <select class="form-select `+`year_month_select`+`" aria-label="Default select example" id="month">
                <option value="-1">請選擇月份</option>
                ` + option + `
                </select>
                <button class="btn btn-outline-primary button_month_chart disabled" type="button">顯示圖表</button>
                </div>
                `;
                _month_select.innerHTML = selectHTML;
                button_month_chart = document.querySelector('.button_month_chart');
                year_month_select = document.querySelector('.year_month_select');
                year_month_select.addEventListener('change', function() {
                    if(year_month_select.value == '-1'){
                        button_month_chart.classList.add('disabled');
                    }else{
                        button_month_chart.classList.remove('disabled');
                    }
                });
                button_month_chart.addEventListener('click', function() {
                    month_select = document.querySelector('.year_month_select').value
                    year_select = document.querySelector('.'+class_name).value
                    console.log(year_select, month_select);
                });
            }
        });
    }
});
