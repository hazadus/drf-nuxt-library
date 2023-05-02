<template>
  <h3 class="header is-size-3 mb-3">
    Добавить книгу
  </h3>

  <form>
    <div class="field">
      <label class="label">
        Название книги
      </label>
      <div class="control">
        <input class="input" type="text" placeholder="Название книги">
      </div>
    </div>

    <BulmaNotification type="warning">
      <div class="icon-text">
        <span class="icon has-text-info is-hidden-mobile">
          <Icon name="mdi:information-variant-circle" />
        </span>
        <span>
          <b>Обратите внимание &mdash; на сайте уже есть книги с похожим названием:</b>
        </span>
      </div>

      <div class="content">
        <ul>
          <li>Книга 1</li>
          <li>Книга 2</li>
          <li>Книга 3</li>
        </ul>
      </div>
    </BulmaNotification>

    <div class="columns">
      <div class="column is-3">
        <div class="field">
          <label class="label">Автор</label>
          <div class="control">
            <div class="select">
              <select>
                <option>Выберите автора</option>
                <option>Пукин Александр Сергеевич</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-3">
        <div class="field">
          <label class="label">Издательство</label>
          <div class="control">
            <div class="select">
              <select>
                <option>Выберите издательство</option>
                <option>Просвещение</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <div class="column is-2">
        <div class="field">
          <label class="label">
            Год издания
          </label>
          <div class="control">
            <input class="input" type="text" placeholder="Год">
          </div>
        </div>
      </div>

      <div class="column is-4">
        <div class="field">
          <label class="label">
            Обложка
          </label>
          <div class="control">
            <div class="file has-name">
              <label class="file-label">
                <input class="file-input" ref="fileInputElement" type="file" name="profile-pic" accept="image/*">
                <span class="file-cta">
                  <span class="file-icon">
                    <Icon name="mdi:file-upload-outline" />
                  </span>
                  <span class="file-label">
                    Выберите файл
                  </span>
                </span>
                <span class="file-name">
                  Имя файла
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="field">
      <label class="label">Содержание</label>
      <div class="control">
        <textarea class="textarea" placeholder="Произведения, включенные в издание"></textarea>
      </div>
    </div>

    <div class="field">
      <label class="label">Описание</label>
      <div class="control">
        <textarea class="textarea" placeholder="Краткое описание издания"></textarea>
      </div>
    </div>

    <div class="columns">
      <div class="column is-6">
        <div class="field">
          <label class="label">Выбранные метки:</label>
          <div class="control">

          </div>
        </div>
      </div>

      <div class="column is-6">
        <div class="field">
          <label class="label">Доступные метки:</label>
          <div class="control">

          </div>
        </div>
      </div>
    </div>

    <div class="field is-grouped">
      <div class="control">
        <button class="button is-link">Добавить книгу</button>
      </div>
      <div class="control">
        <button class="button is-link is-light">Очистить форму</button>
      </div>
    </div>
  </form>
</template>