import {
  Body,
  Controller,
  Get,
  NotFoundException,
  Param,
  Post,
} from '@nestjs/common';
import { BookService } from './book.service';
import { BookCreateDto } from './dto/book-create.dto';
import { BookFilterDto } from './dto/book-filter.dto';
import { I18nService } from 'nestjs-i18n';
import { ApiParam, ApiTags } from '@nestjs/swagger';
import { SearchService } from 'src/search/search.service';

@ApiTags('book')
@Controller('book')
export class BookController {
  constructor(
    private bookService: BookService,
    private i18n: I18nService,
    private searchService: SearchService,
  ) {}

  @Post()
  async create(@Body() dto: BookCreateDto) {
    // Создаем книгу
    const createdBook = await this.bookService.create(dto);

    // Добавляем в индекс
    await this.searchService.addDocument(createdBook);
    return createdBook;
  }

  @Get(':id')
  @ApiParam({ name: 'id', type: 'number' })
  async findOneById(@Param() dto: BookFilterDto) {
    // Проверка на существование в бд
    const bookInDb = await this.bookService.findOneById(dto.id);
    if (!bookInDb) {
      throw new NotFoundException(this.i18n.t('validation.NOT_FOUND'));
    }

    return bookInDb;
  }
}
