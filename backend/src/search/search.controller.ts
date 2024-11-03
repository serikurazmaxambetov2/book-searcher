import {
  BadRequestException,
  Controller,
  Delete,
  Get,
  Post,
  Query,
} from '@nestjs/common';
import { SearchService } from './search.service';
import { ApiQuery, ApiTags } from '@nestjs/swagger';
import { I18nService } from 'nestjs-i18n';

@ApiTags('search')
@Controller('search')
export class SearchController {
  constructor(
    private searchService: SearchService,
    private i18n: I18nService,
  ) { }

  @Post('index')
  async createIndex() {
    const indexInDb = await this.searchService.getIndex();
    if (indexInDb?.book) {
      throw new BadRequestException(this.i18n.t('validation.ALREADY_EXISTS'));
    }

    return await this.searchService.createIndex();
  }

  @Get('index')
  async getIndex() {
    return await this.searchService.getIndex();
  }

  @Delete('index')
  async deleteIndex() {
    return await this.searchService.deleteIndex();
  }

  @Get()
  @ApiQuery({ name: 'page', type: 'number', required: false })
  @ApiQuery({ name: 'text', type: 'string' })
  async search(@Query() { page = 1, text }) {
    const result = await this.searchService.search(text, page);
    return {
      total: result.hits.total['value'],
      data: result.hits.hits.map((hit) => hit._source),
    };
  }
}
